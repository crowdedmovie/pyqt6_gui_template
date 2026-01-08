import sys
from PyQt6.QtWidgets import QApplication
from gui import main_window
from gui.main_window import global_exception_hook, MainWindow


# Apply the hook (crash catcher)
sys.excepthook = global_exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: Set a global app icon
    # app.setWindowIcon(QIcon(":/icons/app_icon.jpg"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
