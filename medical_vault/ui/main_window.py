import os
import time

from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from medical_vault.crypto.hybrid import (
    CryptoError,
    InvalidPasswordError,
    KeyFileNotFoundError,
    build_encrypted_payload,
    decrypt_to_file,
    generate_rsa_keypair,
    persist_encrypted_payload,
)
from medical_vault.ui.pages import DashboardPage, DecryptionPage, EncryptionPage
from medical_vault.ui.styles import STYLE


class QaderCyberVault(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Qader Cyber | Secure Protocol Suite")
        self.showMaximized()
        self.setStyleSheet(STYLE)

        self.priv_key, self.pub_key = generate_rsa_keypair()

        self.dashboard_page = DashboardPage()
        self.encryption_page = EncryptionPage()
        self.decryption_page = DecryptionPage()

        self._init_main_layout()

    def _init_main_layout(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 12)
        sidebar_layout.setSpacing(4)

        logo = QLabel("MEDICAL\nVAULT")
        logo.setObjectName("BrandTitle")
        sidebar_layout.addWidget(logo)

        self.btn_home = QPushButton("Dashboard")
        self.btn_enc = QPushButton("Encryption Center")
        self.btn_dec = QPushButton("Decryption Center")

        for btn in (self.btn_home, self.btn_enc, self.btn_dec):
            btn.setObjectName("NavBtn")
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)

        self.btn_home.setChecked(True)
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        self.pages = QStackedWidget()
        self.pages.setObjectName("ContentPane")
        main_layout.addWidget(self.pages)
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.encryption_page)
        self.pages.addWidget(self.decryption_page)

        self.btn_home.clicked.connect(lambda: self._switch_page(0))
        self.btn_enc.clicked.connect(lambda: self._switch_page(1))
        self.btn_dec.clicked.connect(lambda: self._switch_page(2))

        self.encryption_page.btn_select.clicked.connect(self._select_file_enc)
        self.encryption_page.btn_run.clicked.connect(self._process_encryption)
        self.decryption_page.btn_select.clicked.connect(self._select_file_dec)
        self.decryption_page.btn_run.clicked.connect(self._process_decryption)

    def _switch_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        buttons = (self.btn_home, self.btn_enc, self.btn_dec)
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)

    def _log(self, console, message: str, is_error: bool = False) -> None:
        color = (
            "#b42318"
            if is_error
            else "#1e7e34"
            if "SUCCESS" in message
            else "#2f6ea8"
        )
        timestamp = time.strftime("%H:%M:%S")
        console.append(
            f"<span style='color:{color}'>[{timestamp}] > {message}</span>"
        )

    def _select_file_enc(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select Data")
        if path:
            self.target_enc = path
            self._log(
                self.encryption_page.enc_log,
                f"File Loaded: {os.path.basename(path)}",
            )

    def _select_file_dec(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Secure File",
            "",
            "Secure Files (*.qcyber)",
        )
        if path:
            self.target_dec = path
            self._log(
                self.decryption_page.dec_log,
                f"Secure File Ready: {os.path.basename(path)}",
            )

    def _process_encryption(self) -> None:
        enc = self.encryption_page
        if not getattr(self, "target_enc", None) or not enc.enc_pass.text():
            self._log(enc.enc_log, "Missing Data or Password!", True)
            return

        try:
            start = time.perf_counter()
            payload = build_encrypted_payload(
                self.target_enc,
                enc.enc_pass.text(),
                self.pub_key,
            )
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Secure File",
                "",
                "Secure Files (*.qcyber)",
            )
            if save_path:
                key_path = persist_encrypted_payload(payload, save_path)
                self._log(
                    enc.enc_log,
                    f"SUCCESS: Invisible Key hidden at {os.path.basename(key_path)}",
                )
                self._log(
                    enc.enc_log,
                    f"Process completed in {time.perf_counter() - start:.4f}s",
                )
        except CryptoError as e:
            self._log(enc.enc_log, str(e), True)
        except Exception as e:
            self._log(enc.enc_log, str(e), True)

    def _process_decryption(self) -> None:
        dec = self.decryption_page
        if not getattr(self, "target_dec", None) or not dec.dec_pass.text():
            self._log(dec.dec_log, "Missing File or Password!", True)
            return

        try:
            start = time.perf_counter()
            save, _ = QFileDialog.getSaveFileName(self, "Restore Original File")
            if save:
                decrypt_to_file(
                    self.target_dec,
                    dec.dec_pass.text(),
                    self.priv_key,
                    save,
                )
                self._log(
                    dec.dec_log,
                    f"SUCCESS: Restored in {time.perf_counter() - start:.4f}s",
                )
        except KeyFileNotFoundError as e:
            self._log(dec.dec_log, f"ALERT: {e}", True)
        except InvalidPasswordError as e:
            self._log(dec.dec_log, f"ALERT: {e}", True)
        except CryptoError as e:
            self._log(dec.dec_log, f"ALERT: {e}", True)
        except Exception as e:
            self._log(dec.dec_log, f"ALERT: {e}", True)
