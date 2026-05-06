import struct
from typing import BinaryIO, Optional


def write_chunk(file: BinaryIO, data: bytes) -> None:
    file.write(struct.pack(">I", len(data)) + data)


def read_chunk(file: BinaryIO) -> Optional[bytes]:
    header = file.read(4)
    if not header:
        return None
    (length,) = struct.unpack(">I", header)
    return file.read(length)
