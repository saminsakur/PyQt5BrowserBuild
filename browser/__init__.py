import os
import sys
import json
import sqlite3
import threading

from PyQt5 import QtGui
import browser.app
from PyQt5.QtGui import QFontDatabase, QIcon, QFont

from PyQt5.QtWidgets import QApplication
import browser.main_window


# DB to open
connection = sqlite3.connect("BrowserLocalDB.db", check_same_thread=False)
# connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

# Font
textFont = QFont("sans-serif", 14)

if os.path.isfile("settings.json"):  # If settings file exists, then open it
    with open("settings.json", "r") as f:
        settings_data = json.load(f)
else:  # If settings not exists, then create a new file with default settings
    json_data = json.loads(
        """
    {
        "defaultSearchEngine": "Google",
        "startupPage": "http://127.0.0.1:8888/",
        "newTabPage": "http://127.0.0.1:8888/",
        "homeButtonPage": "http://127.0.0.1:8888/"
    }
    """
    )
    with open("settings.json", "w") as f:
        json.dump(json_data, f, indent=2)
    with open("settings.json", "r") as f:
        settings_data = json.load(f)


def create_app():
    gui_app = QApplication(sys.argv)

    # Disable shortcut in context menu
    gui_app.styleHints().setShowShortcutsInContextMenus(False)

    # Set the window name
    QApplication.setApplicationName("Simple Web Browser")

    # Set the window icon
    QApplication.setWindowIcon(QIcon(os.path.join("Icons", "browser.png")))

    # App styles
    if os.path.isfile(os.path.join("browser", "styles", "styles.css")):
        with open(os.path.join("browser", "styles", "styles.css")) as f:
            gui_app.setStyleSheet(f.read())
    
    QFontDatabase.addApplicationFont(os.path.join("fonts", "fa-solid-900.ttf"))

    window = browser.main_window.mainWindow()
    window.show()

    sys.exit(gui_app.exec_())


def start_server():
    browser.app.app.run(port=8888, debug=False)


def main():
    t1 = threading.Thread(target=create_app)
    t2 = threading.Thread(target=start_server)
    t1.start()
    t2.start()
