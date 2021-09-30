import re
import os
import sys
import json
import sqlite3
import threading
from app import app
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon, QFont

from PyQt5.QtWidgets import QApplication
from .main_window import mainWindow

# Regular expressions to match urls
pattern = re.compile(
    r"^(http|https)?:?(\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)
without_http_pattern = re.compile(
    r"[\-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)
file_pattern = re.compile(r"^file://")

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




"""Settings for user:
    #1 Change default search engine
    #2 Change startup page
    #3 Change page to display on new tab
    #4 Change page to navigate when home button is pressed
"""





def create_app():
    app = QApplication(sys.argv)

    # Disable shortcut in context menu
    app.styleHints().setShowShortcutsInContextMenus(False)

    # Set the window name
    QApplication.setApplicationName("Simple Web Browser")

    # Set the window icon
    QApplication.setWindowIcon(QIcon(os.path.join("Icons", "browser.png")))

    # App styles
    app.setStyleSheet(
        """
    QPushButton#ContextMenuTriggerButn::menu-indicator{ /* Hide context menu button dropdown icon */
        image: none;
    }

    QToolBar {
        background-color: #edf4f7;
    }
    

    /* Style all contextmenus*/

    Qmenu{
        background-color:fff;
    }


    /* Style right arrow of QMenu */

    QMenu::right-arrow{
        image :url(resources/right-arrow-context-menu.png);
        height:12px;
        width:12px;
    }

    QMenu::item{    /* Styling all contextmenus */
        background-color: transparent;
        font-size: 10pt;
        padding-left: 10px;
        padding-right: 100px;
        padding-top:5px;
        padding-bottom: 5px;
        width: 120px;
    }

    QMenu::item:selected{
        background-color: #dedeff;
    }

    /*
     The three dot menu 
    */

    QMenu#ContextMenu {
        background-color: #fdfdfd;
        border: 1px solid transparent;        
        font-family: sans-serif;
        border-radius: 6px;
    }

    QMenu#ContextMenu::item {
        background-color: transparent;
        font-size: 10pt;
        padding-left: 40px;
        padding-right: 100px;
        padding-top:8px;
        padding-bottom: 8px;
        width: 130px;
    }

    QMenu#ContextMenu::icon{
        padding-left:40px;
    }

    QMenu#ContextMenu::separator {
        height: 1px;
        background-color: gray;
        margin-left: 0%;
        margin-right: 0%;
    }

    QMenu#ContextMenu::item:selected{
        background-color: #f2f2f2;
    }

    /*
     Styling of toolip
    */

    QToolTip{
        background-color:#131c21;
        font-size: 10pt;
        opacity:200;
        color: #f1f1f1;
        padding:5px;
        border-width:2px;
        border-style:solid;
        border-radius:20px;
        border: 2px solid transparent;
    }
    

    /* SSLinfo label */

    QLabel#SSLIcon {    /* ssl icon */
        border: 1px solid transparent;
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 6px;
        width: 5px;
        height: 5px;
    }


    /* Button styling */

    QPushButton#ContextMenuTriggerButn {    /* Context menu button */
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 16px;
        width: 10px;
        height: 10px;
        background-color: none;
        margin-left:5px;
        margin-right:5px;
    }

    QPushButton#back_btn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#forward_butn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#reload_butn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#home_button {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#stop_butn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }


    /*
    * after hover
    */

    QPushButton#stop_butn:hover {
        background-color: #dce9ef;
    }

    QPushButton#back_btn:hover {
        background-color: #dce9ef;
    }

    QPushButton#forward_butn:hover {
        background-color: #dce9ef;
    }

    QPushButton#reload_butn:hover {
        background-color: #dce9ef;
    }

    QPushButton#home_button:hover {
        background-color: #dce9ef;
    }

    QPushButton#ContextMenuTriggerButn:hover {
        background-color: #dce9ef;
    }

    /*
    * after pressed
    */

    QPushButton#stop_butn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#back_btn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#forward_butn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#reload_butn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#home_button:pressed {
        background-color: #cadfe7;
    }

    QPushButton#ContextMenuTriggerButn:pressed {
        background-color: #cadfe7;
    }

    """
    )

    window = mainWindow()
    window.show()

    sys.exit(app.exec_())


def start_server():
    app.run(port=8888)


def main():
    t1 = threading.Thread(target=create_app)
    t2 = threading.Thread(target=app.run, kwargs={"port": 8888})
    t1.start()
    t2.start()


