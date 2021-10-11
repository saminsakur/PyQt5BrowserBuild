import os
import sys
import json
import sqlite3

import threading
import browser.app
from PyQt5.QtGui import QFontDatabase, QIcon, QFont

from PyQt5.QtWidgets import QApplication
import browser.main_window


# DB to open
connection = sqlite3.connect("BrowserLocalDB.db", check_same_thread=False)
# connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

# Font
textFont = QFont("Times", 14)

if os.path.isfile("settings.json"):  # If settings file exists, then open it
    with open("settings.json", "r") as f:
        settings_data = json.load(f)
else:  # If settings not exists, then create a new file with default settings
    json_data = json.loads(
        """
    {
        "defaultSearchEngine": "Google",
        "startupPage": "http://google.com/",
        "newTabPage": "http://google.com/",
        "homeButtonPage": "http://google.com/"
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
    QApplication.setWindowIcon(QIcon(os.path.join("resources", "logos", "browser.png")))

    # App styles
    if os.path.isfile(os.path.join("styles", "styles.css")):
        with open(os.path.join("styles", "styles.css")) as f:
            gui_app.setStyleSheet(f.read())
    
    QFontDatabase.addApplicationFont(os.path.join("fonts", "fa-solid-900.ttf"))

    window = browser.main_window.mainWindow()

    sys.exit(gui_app.exec_())


def start_server():
    browser.app.app.run(port=8888)


def main():
    t2 = threading.Thread(target=start_server)
    t1 = threading.Thread(target=create_app)
    t1.start()
    t2.start()
