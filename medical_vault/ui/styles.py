STYLE = """
QMainWindow {
    background-color: #f4f7fb;
    color: #1f2937;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 12px;
}

QWidget#PageContainer {
    background-color: #f4f7fb;
}

QFrame#Sidebar {
    background-color: #ffffff;
    border-right: 1px solid #d6deea;
}

QLabel#BrandTitle {
    color: #1e3a5f;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin: 24px 20px 12px 20px;
}

QPushButton#NavBtn {
    background-color: transparent;
    color: #5f6f84;
    border: 0;
    text-align: left;
    padding: 12px 18px;
    margin: 2px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#NavBtn:hover {
    background-color: #eef3f9;
    color: #1e3a5f;
}

QPushButton#NavBtn:checked {
    color: #1e3a5f;
    background-color: #e3edf8;
}

QWidget#ContentPane {
    background-color: #f4f7fb;
}

QLabel#DashboardTitle {
    color: #1e3a5f;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 0.4px;
}

QLabel#DashboardSubtitle {
    color: #5f6f84;
    font-size: 14px;
    font-weight: 500;
}

QLabel#DeveloperLabel {
    color: #8391a4;
    font-size: 12px;
    font-weight: 600;
    margin-top: 24px;
}

QLabel#PageTitle {
    color: #1e3a5f;
    font-size: 18px;
    font-weight: 700;
    padding-bottom: 4px;
}

QLabel#FieldLabel {
    color: #4f5f75;
    font-size: 12px;
    font-weight: 600;
}

QLineEdit#InputField {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #ccd7e6;
    border-radius: 8px;
    padding: 10px 12px;
}

QLineEdit#InputField:focus {
    border: 1px solid #4a79ad;
}

QPushButton#SecondaryAction {
    background-color: #ffffff;
    color: #1e3a5f;
    border: 1px solid #c8d4e5;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#SecondaryAction:hover {
    background-color: #eef3f9;
}

QPushButton#PrimaryAction {
    background-color: #2f6ea8;
    color: #ffffff;
    border: 1px solid #2f6ea8;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    font-weight: 700;
}

QPushButton#PrimaryAction:hover {
    background-color: #285e90;
}

QPushButton#PrimaryAction:disabled,
QPushButton#SecondaryAction:disabled {
    background-color: #e9eef5;
    color: #9aa7b8;
    border: 1px solid #d9e0ea;
}

QTextEdit#LogConsole {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #ccd7e6;
    border-radius: 8px;
    padding: 8px;
    font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
    font-size: 12px;
}
"""
