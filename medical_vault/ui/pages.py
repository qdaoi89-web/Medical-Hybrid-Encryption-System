from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addStretch()

        title = QLabel("MEDICAL HYBRID ENCRYPTION SYSTEM")
        title.setStyleSheet(
            "color: #38bdf8; font-size: 30px; font-weight: bold; letter-spacing: 1px;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Advanced Cyber-Security Protocol Suite")
        sub.setStyleSheet("color: #64748b; font-size: 16px;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub)

        layout.addStretch()

        dev_label = QLabel("Developed by:\nAbdul-Qader Abbas & Hussein Riyadh")
        dev_label.setStyleSheet(
            "color: #475569; font-size: 13px; font-weight: bold; margin: 30px;"
        )
        dev_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(dev_label)


class EncryptionPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        lbl = QLabel("ENCRYPTION MODULE")
        lbl.setStyleSheet(
            "color: #38bdf8; font-size: 20px; font-weight: bold; padding: 10px;"
        )
        layout.addWidget(lbl)

        self.enc_pass = QLineEdit()
        self.enc_pass.setPlaceholderText("Set Master Security Password...")
        self.enc_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.enc_pass)

        self.btn_select = QPushButton("SELECT MEDICAL DATA")
        layout.addWidget(self.btn_select)

        self.btn_run = QPushButton("EXECUTE ENCRYPTION & HIDE KEY")
        self.btn_run.setStyleSheet(
            "background-color: #38bdf8; color: black; font-weight: bold; padding: 12px;"
        )
        layout.addWidget(self.btn_run)

        self.enc_log = QTextEdit()
        self.enc_log.setReadOnly(True)
        layout.addWidget(self.enc_log)


class DecryptionPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        lbl = QLabel("DECRYPTION PORTAL")
        lbl.setStyleSheet(
            "color: #10b981; font-size: 20px; font-weight: bold; padding: 10px;"
        )
        layout.addWidget(lbl)

        self.dec_pass = QLineEdit()
        self.dec_pass.setPlaceholderText("Enter Master Password...")
        self.dec_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.dec_pass)

        self.btn_select = QPushButton("LOAD SECURE FILE")
        layout.addWidget(self.btn_select)

        self.btn_run = QPushButton("DECRYPT & RESTORE DATA")
        self.btn_run.setStyleSheet(
            "background-color: #10b981; color: black; font-weight: bold; padding: 12px;"
        )
        layout.addWidget(self.btn_run)

        self.dec_log = QTextEdit()
        self.dec_log.setReadOnly(True)
        layout.addWidget(self.dec_log)
