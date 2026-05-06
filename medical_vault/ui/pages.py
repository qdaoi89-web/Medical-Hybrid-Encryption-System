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
        self.setObjectName("PageContainer")
        layout.setContentsMargins(32, 32, 32, 24)
        layout.setSpacing(8)
        layout.addStretch()

        title = QLabel("Medical Hybrid Encryption System")
        title.setObjectName("DashboardTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Clinical-Grade Data Protection Suite")
        sub.setObjectName("DashboardSubtitle")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub)

        layout.addStretch()

        dev_label = QLabel("Developed by:\nAbdul-Qader Abbas & Hussein Riyadh")
        dev_label.setObjectName("DeveloperLabel")
        dev_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(dev_label)


class EncryptionPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PageContainer")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 24)
        layout.setSpacing(12)

        lbl = QLabel("Encryption Center")
        lbl.setObjectName("PageTitle")
        layout.addWidget(lbl)

        pass_label = QLabel("Master Password")
        pass_label.setObjectName("FieldLabel")
        layout.addWidget(pass_label)

        self.enc_pass = QLineEdit()
        self.enc_pass.setObjectName("InputField")
        self.enc_pass.setPlaceholderText("Enter a master password")
        self.enc_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.enc_pass)

        self.btn_select = QPushButton("Select Medical Data File")
        self.btn_select.setObjectName("SecondaryAction")
        layout.addWidget(self.btn_select)

        self.btn_run = QPushButton("Encrypt and Hide Key")
        self.btn_run.setObjectName("PrimaryAction")
        layout.addWidget(self.btn_run)

        self.enc_log = QTextEdit()
        self.enc_log.setObjectName("LogConsole")
        self.enc_log.setReadOnly(True)
        layout.addWidget(self.enc_log)


class DecryptionPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PageContainer")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 24)
        layout.setSpacing(12)

        lbl = QLabel("Decryption Center")
        lbl.setObjectName("PageTitle")
        layout.addWidget(lbl)

        pass_label = QLabel("Master Password")
        pass_label.setObjectName("FieldLabel")
        layout.addWidget(pass_label)

        self.dec_pass = QLineEdit()
        self.dec_pass.setObjectName("InputField")
        self.dec_pass.setPlaceholderText("Enter your master password")
        self.dec_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.dec_pass)

        self.btn_select = QPushButton("Load Secure File")
        self.btn_select.setObjectName("SecondaryAction")
        layout.addWidget(self.btn_select)

        self.btn_run = QPushButton("Decrypt and Restore Data")
        self.btn_run.setObjectName("PrimaryAction")
        layout.addWidget(self.btn_run)

        self.dec_log = QTextEdit()
        self.dec_log.setObjectName("LogConsole")
        self.dec_log.setReadOnly(True)
        layout.addWidget(self.dec_log)
