import sys

from PyQt6.QtWidgets import QApplication

from medical_vault.ui import QaderCyberVault


def main() -> None:
    app = QApplication(sys.argv)
    window = QaderCyberVault()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
