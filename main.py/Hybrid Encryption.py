import sys
import os
import struct
import time
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QFileDialog, QFrame, QStackedWidget, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend

# --- Global Professional Style ---
STYLE = """
QMainWindow { background-color: #020617; }
QFrame#Sidebar { background-color: #0f172a; border-right: 1px solid #1e293b; }
QPushButton#NavBtn { 
    background-color: transparent; color: #94a3b8; border: None; 
    text-align: left; padding: 15px; font-size: 14px; font-weight: bold;
}
QPushButton#NavBtn:checked { color: #38bdf8; border-left: 3px solid #38bdf8; background-color: #1e293b; }
QLineEdit {
    background-color: #1e293b; color: white; border: 1px solid #38bdf8;
    border-radius: 5px; padding: 8px; font-family: 'Consolas';
}
QTextEdit { background-color: #020617; border: 1px solid #1e293b; font-family: 'Consolas'; font-size: 11px; }
"""

class QaderCyberVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qader Cyber | Secure Protocol Suite")
        self.setFixedSize(950, 650)
        self.setStyleSheet(STYLE)

        # Generate System RSA Keys (In-Memory for Demo)
        private_key = rsa.generate_private_key(65537, 2048)
        self.priv_key = private_key
        self.pub_key = private_key.public_key()

        self.init_main_layout()

    def init_main_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Sidebar Navigation
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(self.sidebar)
        
        logo = QLabel("QADER\nCYBER")
        logo.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 22px; margin: 20px;")
        sidebar_layout.addWidget(logo)

        self.btn_home = QPushButton("  DASHBOARD")
        self.btn_enc = QPushButton("  ENCRYPTION ENGINE")
        self.btn_dec = QPushButton("  DECRYPTION PORTAL")
        
        for btn in [self.btn_home, self.btn_enc, self.btn_dec]:
            btn.setObjectName("NavBtn")
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)
        
        self.btn_home.setChecked(True)
        sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        # 2. Pages Container
        self.pages = QStackedWidget()
        self.main_layout.addWidget(self.pages)
        self.create_dashboard()
        self.create_encryption_ui()
        self.create_decryption_ui()

        # Connect Navigation
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        self.btn_enc.clicked.connect(lambda: self.switch_page(1))
        self.btn_dec.clicked.connect(lambda: self.switch_page(2))

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        buttons = [self.btn_home, self.btn_enc, self.btn_dec]
        for i, btn in enumerate(buttons): btn.setChecked(i == index)

    def log(self, console, message, is_error=False):
        color = "#ef4444" if is_error else "#22c55e" if "SUCCESS" in message else "#38bdf8"
        timestamp = time.strftime("%H:%M:%S")
        console.append(f"<span style='color:{color}'>[{timestamp}] > {message}</span>")

    # --- UI Pages ---
    def create_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch()
        
        title = QLabel("MEDICAL HYBRID ENCRYPTION SYSTEM")
        title.setStyleSheet("color: #38bdf8; font-size: 30px; font-weight: bold; letter-spacing: 1px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        sub = QLabel("Advanced Cyber-Security Protocol Suite")
        sub.setStyleSheet("color: #64748b; font-size: 16px;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub)

        layout.addStretch()
        
        dev_label = QLabel("Developed by:\nAbdul-Qader Abbas & Hussein Riyadh")
        dev_label.setStyleSheet("color: #475569; font-size: 13px; font-weight: bold; margin: 30px;")
        dev_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(dev_label)
        self.pages.addWidget(page)

    def create_encryption_ui(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        lbl = QLabel("ENCRYPTION MODULE")
        lbl.setStyleSheet("color: #38bdf8; font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(lbl)

        self.enc_pass = QLineEdit()
        self.enc_pass.setPlaceholderText("Set Master Security Password...")
        self.enc_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.enc_pass)

        btn_sel = QPushButton("SELECT MEDICAL DATA")
        btn_sel.clicked.connect(self.select_file_enc)
        layout.addWidget(btn_sel)

        btn_run = QPushButton("EXECUTE ENCRYPTION & HIDE KEY")
        btn_run.setStyleSheet("background-color: #38bdf8; color: black; font-weight: bold; padding: 12px;")
        btn_run.clicked.connect(self.process_encryption)
        layout.addWidget(btn_run)

        self.enc_log = QTextEdit()
        self.enc_log.setReadOnly(True)
        layout.addWidget(self.enc_log)
        self.pages.addWidget(page)

    def create_decryption_ui(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        lbl = QLabel("DECRYPTION PORTAL")
        lbl.setStyleSheet("color: #10b981; font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(lbl)

        self.dec_pass = QLineEdit()
        self.dec_pass.setPlaceholderText("Enter Master Password...")
        self.dec_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.dec_pass)

        btn_sel = QPushButton("LOAD SECURE FILE")
        btn_sel.clicked.connect(self.select_file_dec)
        layout.addWidget(btn_sel)

        btn_run = QPushButton("DECRYPT & RESTORE DATA")
        btn_run.setStyleSheet("background-color: #10b981; color: black; font-weight: bold; padding: 12px;")
        btn_run.clicked.connect(self.process_decryption)
        layout.addWidget(btn_run)

        self.dec_log = QTextEdit()
        self.dec_log.setReadOnly(True)
        layout.addWidget(self.dec_log)
        self.pages.addWidget(page)

    # --- Logic ---
    def select_file_enc(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Data")
        if path: self.target_enc = path; self.log(self.enc_log, f"File Loaded: {os.path.basename(path)}")

    def select_file_dec(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Secure File", "", "Secure Files (*.qcyber)")
        if path: self.target_dec = path; self.log(self.dec_log, f"Secure File Ready: {os.path.basename(path)}")

    def process_encryption(self):
        if not hasattr(self, 'target_enc') or not self.enc_pass.text():
            self.log(self.enc_log, "Missing Data or Password!", True); return

        try:
            start = time.perf_counter()
            # 1. KDF (Salt & Password)
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            aes_key = kdf.derive(self.enc_pass.text().encode())
            
            # 2. AES-GCM
            with open(self.target_enc, "rb") as f: data = f.read()
            nonce = os.urandom(12)
            cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()

            # 3. RSA Wrapping
            enc_key_rsa = self.pub_key.encrypt(aes_key, asym_padding.OAEP(asym_padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

            # 4. Save Main File
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Secure File", "", "Secure Files (*.qcyber)")
            if save_path:
                with open(save_path, "wb") as f:
                    for i in [nonce, encryptor.tag, ciphertext]: f.write(struct.pack(">I", len(i)) + i)
                
                # 5. Save Secret Invisible Key (The Special Move)
                key_path = save_path + ".sys_dat"
                with open(key_path, "wb") as f:
                    for i in [salt, enc_key_rsa]: f.write(struct.pack(">I", len(i)) + i)
                
                # Hide the key file (Windows Only)
                ctypes.windll.kernel32.SetFileAttributesW(key_path, 0x02)
                
                self.log(self.enc_log, f"SUCCESS: Invisible Key hidden at {os.path.basename(key_path)}")
                self.log(self.enc_log, f"Process completed in {time.perf_counter()-start:.4f}s")
        except Exception as e: self.log(self.enc_log, str(e), True)

    def process_decryption(self):
        if not hasattr(self, 'target_dec') or not self.dec_pass.text():
            self.log(self.dec_log, "Missing File or Password!", True); return

        try:
            start = time.perf_counter()
            # Search for the invisible key
            key_path = self.target_dec + ".sys_dat"
            if not os.path.exists(key_path): raise FileNotFoundError("Security Key Not Found!")

            with open(key_path, "rb") as f:
                def r(file): 
                    s_data = file.read(4)
                    return file.read(struct.unpack(">I", s_data)[0]) if s_data else None
                salt = r(f); enc_key_rsa = r(f)

            # Re-derive & RSA Decrypt
            kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 100000, default_backend())
            derived_key = kdf.derive(self.dec_pass.text().encode())
            aes_key = self.priv_key.decrypt(enc_key_rsa, asym_padding.OAEP(asym_padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

            if derived_key != aes_key: raise ValueError("Access Denied: Invalid Password")

            with open(self.target_dec, "rb") as f:
                nonce = r(f); tag = r(f); ct = r(f)
            
            decryptor = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag)).decryptor()
            original = decryptor.update(ct) + decryptor.finalize()

            save, _ = QFileDialog.getSaveFileName(self, "Restore Original File")
            if save:
                with open(save, "wb") as f: f.write(original)
                self.log(self.dec_log, f"SUCCESS: Restored in {time.perf_counter()-start:.4f}s")
        except Exception as e: self.log(self.dec_log, f"ALERT: {str(e)}", True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QaderCyberVault(); window.show()
    sys.exit(app.exec())