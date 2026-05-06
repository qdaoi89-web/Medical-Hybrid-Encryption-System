from __future__ import annotations

import os
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from medical_vault.crypto import framing
from medical_vault.crypto.platform_fs import hide_file_if_windows


class CryptoError(Exception):
    """Base class for hybrid crypto errors."""


class KeyFileNotFoundError(CryptoError):
    """Raised when the sidecar key file is missing."""


class InvalidPasswordError(CryptoError):
    """Raised when the password does not match the wrapped key."""


@dataclass(frozen=True)
class EncryptedPayload:
    salt: bytes
    enc_key_rsa: bytes
    nonce: bytes
    tag: bytes
    ciphertext: bytes


def generate_rsa_keypair() -> tuple[RSAPrivateKey, RSAPublicKey]:
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()


def _derive_aes_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


def build_encrypted_payload(
    plaintext_path: str,
    password: str,
    public_key: RSAPublicKey,
) -> EncryptedPayload:
    salt = os.urandom(16)
    aes_key = _derive_aes_key(password, salt)

    with open(plaintext_path, "rb") as f:
        data = f.read()

    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()

    enc_key_rsa = public_key.encrypt(
        aes_key,
        asym_padding.OAEP(
            asym_padding.MGF1(algorithm=hashes.SHA256()),
            hashes.SHA256(),
            None,
        ),
    )

    return EncryptedPayload(
        salt=salt,
        enc_key_rsa=enc_key_rsa,
        nonce=nonce,
        tag=encryptor.tag,
        ciphertext=ciphertext,
    )


def persist_encrypted_payload(payload: EncryptedPayload, ciphertext_path: str) -> str:
    key_path = ciphertext_path + ".sys_dat"
    with open(ciphertext_path, "wb") as f:
        for chunk in (payload.nonce, payload.tag, payload.ciphertext):
            framing.write_chunk(f, chunk)

    with open(key_path, "wb") as f:
        for chunk in (payload.salt, payload.enc_key_rsa):
            framing.write_chunk(f, chunk)

    hide_file_if_windows(key_path)
    return key_path


def decrypt_to_file(
    ciphertext_path: str,
    password: str,
    private_key: RSAPrivateKey,
    output_path: str,
) -> None:
    key_path = ciphertext_path + ".sys_dat"
    if not os.path.exists(key_path):
        raise KeyFileNotFoundError("Security Key Not Found!")

    with open(key_path, "rb") as f:
        salt = framing.read_chunk(f)
        enc_key_rsa = framing.read_chunk(f)
    if salt is None or enc_key_rsa is None:
        raise CryptoError("Corrupt key sidecar file.")

    derived_key = _derive_aes_key(password, salt)
    aes_key = private_key.decrypt(
        enc_key_rsa,
        asym_padding.OAEP(
            asym_padding.MGF1(algorithm=hashes.SHA256()),
            hashes.SHA256(),
            None,
        ),
    )

    if derived_key != aes_key:
        raise InvalidPasswordError("Access Denied: Invalid Password")

    with open(ciphertext_path, "rb") as f:
        nonce = framing.read_chunk(f)
        tag = framing.read_chunk(f)
        ct = framing.read_chunk(f)
    if nonce is None or tag is None or ct is None:
        raise CryptoError("Corrupt ciphertext file.")

    decryptor = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(nonce, tag),
    ).decryptor()
    original = decryptor.update(ct) + decryptor.finalize()

    with open(output_path, "wb") as f:
        f.write(original)
