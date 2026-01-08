
import sys
import os
import traceback
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from .gui_interface import Ui_Main
from .icons import resources_rc

# --- CRASH CATCHER ---
def global_exception_hook(exctype, value, tb):
    """
    Catches any unhandled exception and displays a GUI error message.
    This prevents the app from silently vanishing.
    """
    traceback_formated = ''.join(traceback.format_exception(exctype, value, tb))
    
    # Still print to console for IDE debugging
    print(traceback_formated, file=sys.stderr)
    
    # Create the error dialog
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Icon.Critical)
    error_box.setWindowTitle("Critical Error")
    error_box.setText("An unexpected error occurred.")
    error_box.setInformativeText(str(value)) # The short error message
    error_box.setDetailedText(traceback_formated) # The full stack trace
    error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_box.exec()
    
    # Optional: Exit app after error, or let user try to continue
    sys.exit(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
    
        self.current_theme = "dark"
        self.set_theme(self.current_theme)

        # Connect menu actions for theme switching
        self.ui.actionDark.triggered.connect(lambda: self.set_theme("dark"))
        self.ui.actionLight.triggered.connect(lambda: self.set_theme("light"))
        self.ui.actionToggle_Theme_Ctrl_T.triggered.connect(self.toggle_theme)
        self.ui.actionToggle_Theme_Ctrl_T.setShortcut("Ctrl+T")        

        # Connect menu actions for help/about
        self.ui.actionAbout.triggered.connect(self.show_about_popup)
        self.ui.actionUsage.triggered.connect(self.show_usage_popup)

        # Close the app
        self.ui.actionExit.triggered.connect(self.close)

    def show_usage_popup(self):
        """Displays the Usage popup."""
        usage_text = (
            "<h3>Application Template Usage</h3>"
            "<ul>"
            "<li><b>Theming:</b> Go to <i>View > Theme</i> to toggle modes(or Ctrl+T).</li>"
            "<li><b>Expansion:</b> Add widgets to the central layout.</li>"
            "</ul>"
        )
        # QMessageBox.information(parent, title, text)
        QMessageBox.information(self, "Usage Guide", usage_text)
    
    def show_about_popup(self):
        """Displays the About popup."""
        about_text = (
            "<h3>PyQt6 App Template</h3>"
            "<p>Version 1.0.0</p>"
            "<p>A modern GUI template featuring Dark/Light themes & icons.</p>"
            "<p>Created by <b>crowdedmovie</b></p>"
            "<br>"
            "<p>View Source on GitHub :</p>"
            "<p><a href='https://github.com/crowdedmovie/pyqt6_gui_template'>https://github.com/crowdedmovie/pyqt6_gui_template</a></p>"
        )
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def set_theme(self, theme_name):
        """
        Applies the CSS file and refreshes all icons.
        theme_name: 'dark' or 'light'
        """
        self.current_theme = theme_name

        # Construct path: project_root/themes/dark.css
        css_file = os.path.join("themes", f"{theme_name}.css")
        script_dir = os.path.dirname(__file__)
        css_file = os.path.join(script_dir, "themes", f"{theme_name}.css")

        try:
            with open(css_file, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: Could not find theme file at {css_file}")

        self.refresh_icons()

    def refresh_icons(self):
        """
                Updates icons using the INVERSE of the current theme.
                Dark Theme -> Uses 'light' icons folder
                Light Theme -> Uses 'dark' icons folder
        """
        if self.current_theme == "dark":
            icon_folder = 'light'
        else:
            icon_folder = 'dark'

        # Search for widgets
        target_objects = self.findChildren(QWidget) + self.findChildren(QAction)

        found_any = False
        for obj in target_objects:
            icon_name = obj.property("icon_name")

            if icon_name:
                found_any = True
                # Construct path
                icon_path = f":/icons/{icon_folder}/{icon_name}.svg"

                # Check if it exists
                new_icon = QIcon(icon_path)

                if new_icon.isNull():
                    #print(f"[FAIL] Could not load: {icon_path}")
                    #print(f"       (Object: {obj.objectName()})")
                    pass
                else:
                    # print(f"[OK]   Loaded: {icon_path}")
                    obj.setIcon(new_icon)

        if not found_any:
            #print("[INFO] No widgets with 'icon_name' property found.")
            pass

    def toggle_theme(self):
        """
        Switches between light and dark mode.
        """
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme(new_theme)
