"""
Simple Web Browser

Chromium based tabbed browser built with PyQt5 QWebEngineView
Made by     - Samin Sakur
Learn more  - https://github.com/saminsakur/PyQt5BrowserBuild/
"""

import re
import os
import sys
import datetime
import sqlite3
import json
from PyQt5 import QtWidgets
import pyperclip as pc

from PyQt5 import QtGui, QtCore
from PyQt5.QtWebEngineWidgets import *

from PyQt5.QtGui import (
    QColor,
    QIcon,
    QFont,
    QPainter,
    QPixmap
)

from PyQt5.QtCore import (
    QUrl,
    Qt,
    QSize,
    QObject,
    pyqtSlot,
    QEventLoop,
    QPointF
)

from PyQt5.QtWidgets import (
    QComboBox,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QTabWidget,
    QLineEdit,
    QMenu,
    QLabel,
    QToolBar,
    QMessageBox,
    QDialogButtonBox,
    QDialog,
    QProgressDialog,
    QProgressBar,
    QWidget,
    QPushButton,
    QListWidget,
    QGridLayout,
    QMainWindow,
    QVBoxLayout,
    QShortcut,
    QAction,
    QFileDialog,
    QApplication
)

from PyQt5.QtPrintSupport import (
    QPrinter,
    QPrintDialog,
    QPrintPreviewDialog
)

# Regular expressions to match urls
pattern = re.compile(
    r"^(http|https)?:?(\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
without_http_pattern = re.compile(
    r"[\-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
file_pattern = re.compile(r"^file://")

# DB to open
connection = sqlite3.connect("BrowserLocalDB.db")
# connection = sqlite3.connect(":memory:")

cursor = connection.cursor()

# Font
textFont = QFont("sans-serif", 14)
if os.path.isfile("settings.json"):  # If settings file exists, then open it
    with open("settings.json", "r") as f:
        settings_data = json.load(f)
else:  # If settings not exists, then create a new file with default settings
    json_data = json.loads("""{
        "defaultSearchEngine": "Google",
        "startupPage": "https://www.google.com/",
        "newTabPage": "https://www.google.com/",
        "homeButtonPage": "https://www.google.com/"
    }
    """)
    with open("settings.json", "w") as f:
        json.dump(json_data, f, indent=2)
    with open("settings.json", "r") as f:
        settings_data = json.load(f)


class fileErrorDialog (QMessageBox):
    def __init__(self, *args, **kwargs):
        super(fileErrorDialog, self).__init__(*args, **kwargs)

        self.setText("Wrong file entered, Enter a correct file and try again.")
        self.setIcon(QMessageBox.Critical)

        self.setWindowTitle("Please enter a correct file")
        self.show()


class errorMsg (QMessageBox):
    def __init__(self, text: str = "An internal error occurred!"):
        super(errorMsg, self).__init__()

        self.setText(text)
        self.setIcon(QMessageBox.Critical)

        self.setWindowTitle("Error!")
        self.show()


class mainWindow (QMainWindow):

    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__(*args, **kwargs)

        # create tabs
        self.tabs = Tabs()

        # create history table
        cursor.execute("""CREATE TABLE IF NOT EXISTS "history" (
                   "id"	INTEGER,
                   "title"	TEXT,
                   "url"	TEXT,
                   "date"	TEXT,
               	PRIMARY KEY("id")
               	)""")

        # Add new tab when tab tab is doubleclicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # To connect to a function when current tab has been changed
        self.tabs.currentChanged.connect(self.tab_changed)

        # Function to handle tab closing
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # open new tab when Ctrl+T pressed
        AddNewTabKeyShortcut = QShortcut("Ctrl+T", self)
        AddNewTabKeyShortcut.activated.connect(lambda: self.add_new_tab(
            QtCore.QUrl(settings_data["newTabPage"], "New tab")))

        # Close current tab on Ctrl+W
        CloseCurrentTabKeyShortcut = QShortcut("Ctrl+W", self)
        CloseCurrentTabKeyShortcut.activated.connect(
            lambda: self.close_current_tab(self.tabs.currentIndex()))

        # Exit browser on shortcut Ctrl+Shift+W
        ExitBrowserShortcutKey = QShortcut("Ctrl+Shift+W", self)
        ExitBrowserShortcutKey.activated.connect(sys.exit)

        # nav bar
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.addToolBar(self.navbar)

        # back button
        back_btn = QPushButton(self)
        back_btn.setObjectName("back_btn")
        back_btn.setIcon(QtGui.QIcon(
            os.path.join("resources", "left-arrow.png")))
        back_btn.setToolTip("Back to previous page")
        back_btn.setShortcut("Alt+Left")
        back_btn.clicked.connect(self.navigate_back_tab)
        self.navbar.addWidget(back_btn)

        # forward button
        forward_butn = QPushButton(self)
        forward_butn.setObjectName("forward_butn")
        forward_butn.setIcon(QtGui.QIcon(
            os.path.join("resources", "right-arrow.png")))
        forward_butn.setToolTip("Go forward")
        forward_butn.setShortcut("Alt+Right")
        forward_butn.clicked.connect(self.forward_tab)
        self.navbar.addWidget(forward_butn)

        # Refresh button
        self.reload_butn = QPushButton(self)
        self.reload_butn.setObjectName("reload_butn")
        self.reload_butn.setToolTip("Reload current page")
        self.reload_butn.setShortcut("Ctrl+R")
        self.reload_butn.resize(QSize(50, 50))
        self.reload_butn.setIcon(QtGui.QIcon(
            os.path.join("resources", "refresh.png")))
        self.reload_butn.clicked.connect(self.reload_tab)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setObjectName("stop_butn")
        self.stop_btn.setToolTip("Stop loading current page")
        self.stop_btn.setShortcut("Escape")
        self.stop_btn.setIcon(QIcon(os.path.join('resources', 'cross.png')))
        self.stop_btn.clicked.connect(self.stop_loading_tab)

        # Added stop button
        self.stop_action = self.navbar.addWidget(self.stop_btn)

        # Added reload button
        self.reload_action = self.navbar.addWidget(self.reload_butn)

        # Home button
        self.home_button = QPushButton(self)
        self.home_button.setObjectName("home_button")
        self.home_button.setToolTip("Back to home")
        self.home_button.setIcon(QtGui.QIcon(
            os.path.join("resources", "home.png")))
        self.home_button.clicked.connect(self.goToHome)
        self.navbar.addWidget(self.home_button)

        # Add Address bar
        self.url_bar = AddressBar()
        self.url_bar.initAddressBar()
        self.url_bar.setFrame(False)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setShortcutEnabled(True)
        self.url_bar.setToolTip(self.url_bar.text())

        # Set focus on the Addressbar by pressing Ctrl+E
        FocusOnAddressBar = QShortcut("Ctrl+E", self)
        FocusOnAddressBar.activated.connect(self.url_bar.setFocus)

        # Set stop action to be invisible
        self.stop_action.setVisible(False)

        # Add a separator
        self.navbar.addSeparator()

        # Shows ssl security icon
        self.httpsicon = SSLIcon()

        # Add http icon to the navbar bar
        self.navbar.addWidget(self.httpsicon)

        # Add Address Bar to the navbar
        self.navbar.addWidget(self.url_bar)

        # The context menu
        context_menu = QMenu(self)

        # Set the object's name
        context_menu.setObjectName("ContextMenu")

        # Button for the three dot context menu button
        ContextMenuButton = QPushButton(self)
        ContextMenuButton.setObjectName("ContextMenuButton")

        # Enable three dot menu by pressing Alt+F
        ContextMenuButton.setShortcut("Alt+F")

        # Give the three dot image to the Qpushbutton
        ContextMenuButton.setIcon(
            QIcon(os.path.join("resources", "more.png")))  # Add icon
        ContextMenuButton.setObjectName("ContextMenuTriggerButn")
        ContextMenuButton.setToolTip("More")

        # Add the context menu to the three dot context menu button
        ContextMenuButton.setMenu(context_menu)

        """Actions of the three dot context menu"""

        # Add new tab
        newTabAction = QAction("New tab", self)
        newTabAction.setIcon(QtGui.QIcon(
            os.path.join("resources", "newtab.png")))
        newTabAction.triggered.connect(lambda: self.add_new_tab(
            QUrl(settings_data["newTabPage"]), "Homepage"))
        newTabAction.setToolTip("Add a new tab")
        context_menu.addAction(newTabAction)

        # New window action
        newWindowAction = QAction("New window", self)
        newWindowAction.setIcon(QtGui.QIcon(
            os.path.join("resources", "app_window_ios.png")))
        newWindowAction.triggered.connect(self.CreateNewWindow)
        context_menu.addAction(newWindowAction)

        # Close tab action
        CloseTabAction = QAction("Close tab", self)
        CloseTabAction.setIcon(
            QIcon(os.path.join("resources", "closetab.png")))
        CloseTabAction.triggered.connect(
            lambda: self.close_current_tab(self.tabs.currentIndex()))
        CloseTabAction.setToolTip("Close current tab")
        context_menu.addAction(CloseTabAction)

        # A separator
        context_menu.addSeparator()

        # Another separator
        context_menu.addSeparator()

        # Feature to copy site url
        CopySiteAddress = QAction(QtGui.QIcon(os.path.join(
            "resources", "url.png")), "Copy site url", self)
        CopySiteAddress.triggered.connect(self.CopySiteLink)
        CopySiteAddress.setToolTip("Copy current site address")
        context_menu.addAction(CopySiteAddress)

        # Fetaure to go to copied site url
        PasteAndGo = QAction(QtGui.QIcon(os.path.join(
            "resources", "paste.png")), "Paste and go", self)
        PasteAndGo.triggered.connect(self.PasteUrlAndGo)
        PasteAndGo.setToolTip("Go to the an url copied to your clipboard")
        context_menu.addAction(PasteAndGo)

        # A separator
        context_menu.addSeparator()

        # View history
        ViewHistory = QAction("History", self)
        ViewHistory.setIcon(QIcon(os.path.join("resources", "history.png")))
        ViewHistory.triggered.connect(self.openHistory)
        ViewHistory.setShortcut("Ctrl+h")
        context_menu.addAction(ViewHistory)

        # Open page
        OpenPgAction = QAction("Open", self)
        OpenPgAction.setIcon(QtGui.QIcon(
            os.path.join("resources", "openclickhtml.png")))
        OpenPgAction.setToolTip("Open a file in this browser")
        OpenPgAction.setShortcut("Ctrl+O")
        OpenPgAction.triggered.connect(self.open_local_file)
        context_menu.addAction(OpenPgAction)

        # Save page as
        SavePageAs = QAction("Save page as", self)
        SavePageAs.setIcon(QtGui.QIcon(
            os.path.join("resources", "save-disk.png")))
        SavePageAs.setToolTip("Save current page to this device")
        SavePageAs.setShortcut("Ctrl+S")
        SavePageAs.triggered.connect(self.save_page)
        context_menu.addAction(SavePageAs)

        # Print this page action
        PrintThisPageAction = QAction("Print this page", self)
        PrintThisPageAction.setIcon(QtGui.QIcon(
            os.path.join("resources", "printer.png")))
        PrintThisPageAction.triggered.connect(self.print_this_page)
        PrintThisPageAction.setShortcut("Ctrl+P")
        PrintThisPageAction.setToolTip("Print current page")
        context_menu.addAction(PrintThisPageAction)

        # Print with preview
        PrintPageWithPreview = QAction(QtGui.QIcon(os.path.join(
            "resources", "printerprev.png")), "Print page with preview", self)
        PrintPageWithPreview.triggered.connect(self.PrintWithPreview)
        PrintPageWithPreview.setShortcut("Ctrl+Shift+P")
        context_menu.addAction(PrintPageWithPreview)

        # Save page as PDF
        SavePageAsPDF = QAction(QtGui.QIcon(os.path.join(
            "resources", "adobepdf.png")), "Save as PDF", self)
        SavePageAsPDF.triggered.connect(self.save_as_pdf)
        context_menu.addAction(SavePageAsPDF)

        context_menu.addSeparator()

        # Settings widget:
        userSettingsAction = QAction(QtGui.QIcon(os.path.join(
            "resources", "settings_icon.png")), "Settings", self)
        userSettingsAction.triggered.connect(self.openSettings)
        context_menu.addAction(userSettingsAction)

        # The help submenu
        HelpMenu = QMenu("Help", self)
        HelpMenu.setObjectName("HelpMenu")
        HelpMenu.setStyleSheet(
            """
        background-color: #fff;
        background-color: #fdfdfd;
        border: 1px solid transparent;        
        font-family: Times, sans-serif;
        border-radius: 6px;

        QMenu#HelpMenu::item{
            background-color: transparent;
            font-size: 10pt;
            padding-left: 40px;
            padding-right: 100px;
            padding-top:10px;
            padding-bottom: 10px;
            width: 130px;
        }

        QMenu#HelpMenu::item:selected{
            background-color: #f2f2f2;
        }

        QMenu#HelpMenu::icon{
            padding-left:40px;
        }

        """)

        HelpMenu.setIcon(QIcon(os.path.join("resources", "question.png")))

        # About action
        AboutAction = QAction("About this browser", self)
        AboutAction.setIcon(QIcon(os.path.join("resources", "info.png")))
        AboutAction.triggered.connect(self.about)
        HelpMenu.addAction(AboutAction)

        # Visit action
        VisitGithubAction = QAction("Visit Github", self)
        VisitGithubAction.triggered.connect(self.visitGithub)
        HelpMenu.addAction(VisitGithubAction)

        context_menu.addMenu(HelpMenu)

        # Add a separator
        context_menu.addSeparator()

        # Close browser
        CloseBrowser = QAction("Close browser", self)
        CloseBrowser.triggered.connect(lambda: sys.exit())
        context_menu.addAction(CloseBrowser)

        """ 
        Set menu for the button
        ContextMenuButton.add
        Add the context menu to the navbar
        """

        self.navbar.addWidget(ContextMenuButton)

        # Stuffs to see at startup
        self.add_new_tab(QUrl(settings_data["startupPage"]), "Homepage")

        # Set the address focus
        self.url_bar.setFocus()

        # what to display on the window
        self.setCentralWidget(self.tabs)

        # Stuffs to set the window
        self.showMaximized()

        # Set minimum size
        self.setMinimumWidth(400)

    """
    Instead of managing 2 slots associated with the progress and completion of loading,
    only one of them should be used since, for example, the associated slot is also called when
    it is loaded at 100% so it could be hidden since it can be invoked together with finished.
    """

    @QtCore.pyqtSlot(int)
    def loadProgressHandler(self, prog):
        if self.tabs.currentWidget() is not self.sender():
            return

        loading = prog < 100

        self.stop_action.setVisible(loading)
        self.reload_action.setVisible(not loading)

    # funcion to navigate to home when home icon is pressed

    def goToHome(self):
        self.tabs.currentWidget().setUrl(QUrl(settings_data["homeButtonPage"]))

    # Define open a new window

    def CreateNewWindow(self):
        window = mainWindow()
        window.show()

    # Copy url of currently viewed page to clipboard
    def CopySiteLink(self):
        pc.copy(self.tabs.currentWidget().url().toString())

    # Adds a new tab and load the content of the clipboard

    def PasteUrlAndGo(self):
        self.add_new_tab(QUrl(pc.paste()), self.tabs.currentWidget().title())

    # Remove this if you don't need it

    def visitGithub(self):
        self.add_new_tab(
            QUrl("https://github.com/saminsakur/PyQt5BrowserBuild"), "Github")

    # navigate backward tab

    def navigate_back_tab(self):
        self.tabs.currentWidget().back()

    # go forward tab

    def forward_tab(self):
        self.tabs.currentWidget().forward()

    # reload tab

    def reload_tab(self):
        self.tabs.currentWidget().reload()

    # stop load current tab

    def stop_loading_tab(self):
        if self.tabs.currentWidget() is None:
            return

        self.tabs.currentWidget().stop()

    """
    Functions to open a local file and save a website to user's local storage
    """

    # Function to open a local file

    def open_local_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open file",
            directory="",
            filter="Hypertext Markup Language (*.htm *.html *.mhtml);;All files (*.*)"
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf8") as f:
                    opened_file = f.read()
                    self.tabs.currentWidget().setHtml(opened_file)

            except:
                dlg = fileErrorDialog()
                dlg.exec_()

        self.url_bar.setText(filename)

    # Function to save current site to user's local storage

    def save_page(self):
        filepath, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save Page As",
            directory="",
            filter="Webpage, complete (*.htm *.html);;Hypertext Markup Language (*.htm *.html);;All files (*.*)",
        )
        try:
            if filter == "Hypertext Markup Language (*.htm *.html)":
                self.tabs.currentWidget().page().save(
                    filepath, format=QWebEngineDownloadItem.MimeHtmlSaveFormat)

            elif filter == "Webpage, complete (*.htm *.html)":
                self.tabs.currentWidget().page().save(
                    filepath, format=QWebEngineDownloadItem.CompleteHtmlSaveFormat)

        except:
            self.showErrorDlg()

    # Print handler
    def print_this_page(self):
        try:
            handler_print = PrintHandler()
            handler_print.setPage(self.tabs.currentWidget().page())
            handler_print.print()

        except:
            self.showErrorDlg()

    # Print page with preview

    def PrintWithPreview(self):
        handler = PrintHandler()
        handler.setPage(self.tabs.currentWidget().page())
        handler.printPreview()

    # Save as pdf
    def save_as_pdf(self):
        filename, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save as",
            filter="PDF File (*.pdf);;All files (*.*)"
        )

        self.tabs.currentWidget().page().printToPdf(filename)

    # doubleclick on empty space for new tab

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab(
                QUrl(settings_data["newTabPage"]), label="New tab")

    # to update the tab

    def tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    # to close current tab

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    # Update window title

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()

        if 0 > len(title):
            self.setWindowTitle("{} - Simple Web Browser".format(title))

        else:
            self.setWindowTitle("Simple Web Browser")

    # To close current tab

    def close_tab(self, i):
        self.tabs.removeTab(i)

    # function to add new tab

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl(settings_data["newTabPage"])

        browser = QWebEngineView()  # Define the main webview to browser the internet

        # Set page
        browser.setPage(customWebEnginePage(browser))

        # Full screen enble
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        browser.page().fullScreenRequested.connect(lambda request: request.accept())

        browser.loadProgress.connect(self.loadProgressHandler)

        browser.page().WebAction()

        browser.settings().setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.load(qurl)
        self.url_bar.setFocus()

        # update url when it's from the correct tab
        # update url when it's from the correct tab
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

        # update history when loading finished
        browser.page().loadFinished.connect(self.updateHistory)

    def showErrorDlg(self):
        dlg = errorMsg()
        dlg.exec_()

    def about(self):
        self.AboutDialouge = AboutDialog()
        self.AboutDialouge.setWindowFlag(Qt.FramelessWindowHint)
        radiusx = 10.0
        radiusy = 10.0
        path = QtGui.QPainterPath()
        self.AboutDialouge.resize(500, 270)
        path.addRoundedRect(QtCore.QRectF(
            self.AboutDialouge.rect()), radiusx, radiusy)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.AboutDialouge.setMask(mask)

        self.AboutDialouge.exec_()

    # Update address bar to show current pages's url

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            # if signal is not from the current tab, then ignore
            return

        if q.scheme() == 'https':
            # secure padlock icon
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("resources", "security.png")))
            self.httpsicon.setToolTip(
                "Connection to this is is secure\n\nThis site have a valid certificate")

        elif q.scheme() == "file":
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("resources", "file-protocol.png")))
            self.httpsicon.setToolTip("You are viewing a local or shared file")

        elif q.scheme() == "data":
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("resources", "file-protocol.png")))
            self.httpsicon.setToolTip("You are viewing a local or shared file")

        else:
            # Set insecure padlock
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("resources", "warning1.png")))
            self.httpsicon.setToolTip(
                "Connection to this site may not be secured")

        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    # function to search google from the search box
    def searchWeb(self, text):
        Engine = settings_data["defaultSearchEngine"]
        if text:
            if Engine == "Google":
                return "https://www.google.com/search?q=" + "+".join(text.split())

            elif Engine == "Yahoo":
                return "https://search.yahoo.com/search?q=" + "+".join(text.split())

            elif Engine == "Bing":
                return "https://www.bing.com/search?q=" + "+".join(text.split())

            elif Engine == "DuckDuckGo":
                return "https://duckduckgo.com/?q=" + "+".join(text.split())

    """
    function to navigate to url, if the url ends with the domains from the domains tuple,
    then "http://" will be added after what the user have written if not, then it will call
    the searchWeb() function to search bing directly from the search box
    """

    def navigate_to_url(self):
        in_url = self.url_bar.text()
        url = ""
        """ if the text in the search box endswith one of the domain in the domains tuple, then "http://" will be added
         if the text is pre "http://" or "https://" added, then not"""
        # [0-9A-Za-z]+\.+[A-Za-z0-9]{2}

        if self.tabs.currentWidget is None:  # To avoid exception
            # If QTabWidget's currentwidet is none, the ignore
            return

        if file_pattern.search(in_url):
            file_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.tabs.currentWidget().load(local_url)

        elif without_http_pattern.search(in_url) and any([i in in_url for i in ["http://", "https://"]]):
            url = in_url

        elif pattern.search(in_url) and not any(i in in_url for i in ("http://", "https://", "file:///")):
            url = "http://" + in_url

        # this will search google
        elif not "/" in in_url:
            url = self.searchWeb(in_url)

        self.tabs.currentWidget().load(QUrl.fromUserInput(url))

    def updateHistory(self):
        title = self.tabs.currentWidget().page().title()
        url = str(self.tabs.currentWidget().page().url())
        url = url[19:len(url) - 2]
        hour = datetime.datetime.now().strftime("%X")
        day = datetime.datetime.now().strftime("%x")
        date = hour + " - " + day

        data = cursor.execute("SELECT * FROM history")
        siteInfoList = data.fetchall()

        for i in range(len(siteInfoList)):
            if url == siteInfoList[i][2]:
                cursor.execute("DELETE FROM history WHERE url = ?", [url])

        cursor.execute("INSERT INTO history (title,url,date) VALUES (:title,:url,:date)",
                       {"title": title, "url": url, "date": date})

        connection.commit()

    def openHistory(self):
        self.historyWindow = HistoryWindow()
        self.historyWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.historyWindow.setGeometry(
            int(self.tabs.currentWidget().frameGeometry().width() / 2 + 300), 87, 500, 500)
        radiusx = 10.0
        radiusy = 5.0
        path = QtGui.QPainterPath()
        self.historyWindow.resize(370, 490)
        path.addRoundedRect(QtCore.QRectF(
            self.historyWindow.rect()), radiusx, radiusy)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.historyWindow.setMask(mask)

        self.historyWindow.setStyleSheet(
            """
            background-color:#edf4f7;
            """
        )
        self.historyWindow.show()

    def openSiteHistoryClicked(self, url, *args):
        self.tabs.currentWidget().load(url)

    def openSettings(self):
        self.userSettingswindow = UserSettings()
        self.userSettingswindow.setWindowFlag(Qt.FramelessWindowHint)

        # Adding shadows
        effect = QGraphicsDropShadowEffect()
        self.userSettingswindow.setAttribute(Qt.WA_TranslucentBackground)
        effect.setBlurRadius(70)
        self.userSettingswindow.setGraphicsEffect(effect)
        radiusx = 10.0
        radiusy = 5.0
        path = QtGui.QPainterPath()
        self.userSettingswindow.setContentsMargins(0, 0, 0, 0)
        path.addRoundedRect(QtCore.QRectF(
            self.userSettingswindow.rect()), radiusx, radiusy)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.userSettingswindow.setMask(mask)
        self.userSettingswindow.show()


"""Settings for user:
    #1 Change default search engine
    #2 Change startup page
    #3 Change page to display on new tab
    #4 Change page to navigate when home button is pressed
"""


class UserSettings (QWidget):
    def __init__(self):
        super().__init__()
        self.default_search_engine = settings_data["defaultSearchEngine"]
        self.mainWidget = QWidget(self)

        self.init_ui()
        self.retranslateUi()

    def init_ui(self):
        self.resize(706, 485)
        self.addDefaultSearchEngineSelector()

        # Add settings title
        self.label_2 = QtWidgets.QLabel(self.mainWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(
            "font: 12pt \"Segoe UI\";")
        self.label_2.setObjectName("label_2")

        # Close button
        self.closeButn = QtWidgets.QPushButton(self.mainWidget)
        self.closeButn.setGeometry(QtCore.QRect(660, 10, 33, 33))
        self.closeButn.setIcon(QtGui.QIcon(
            os.path.join("resources", "cross.png")))
        self.closeButn.setObjectName("closeButn")
        self.closeButn.clicked.connect(self.closeWindow)

        self.startup_page = QtWidgets.QLineEdit(self.mainWidget)
        self.startup_page.setGeometry(QtCore.QRect(480, 150, 211, 33))
        self.startup_page.setText(settings_data["startupPage"])
        self.startup_page.setObjectName("startup_page")

        # On startup section
        self.label_3 = QtWidgets.QLabel(self.mainWidget)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label = QtWidgets.QLabel(self.mainWidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Home button section
        self.label_7 = QtWidgets.QLabel(self.mainWidget)
        self.label_7.setGeometry(QtCore.QRect(10, 230, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        # Home button page
        self.home_button_page = QtWidgets.QLineEdit(self.mainWidget)
        self.home_button_page.setGeometry(QtCore.QRect(480, 250, 211, 33))
        self.home_button_page.setText(settings_data["homeButtonPage"])
        self.home_button_page.setObjectName("home_button_page")

        # New tab open settings
        self.label_9 = QtWidgets.QLabel(self.mainWidget)
        self.label_9.setGeometry(QtCore.QRect(10, 330, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        # Page to open on each tab
        self.new_tab_page = QtWidgets.QLineEdit(self.mainWidget)
        self.new_tab_page.setText(settings_data["newTabPage"])
        self.new_tab_page.setGeometry(QtCore.QRect(480, 360, 211, 33))
        self.new_tab_page.setObjectName("new_tab_page")

        # these are all descriptions
        self.label_4 = QtWidgets.QLabel(self.mainWidget)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 235, 20))
        self.label_4.setObjectName("label_4")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_4.setFont(font)

        self.label_5 = QtWidgets.QLabel(self.mainWidget)
        self.label_5.setGeometry(QtCore.QRect(10, 90, 270, 20))
        self.label_5.setObjectName("label_5")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_5.setFont(font)

        self.label_6 = QtWidgets.QLabel(self.mainWidget)
        self.label_6.setGeometry(QtCore.QRect(10, 260, 360, 20))
        self.label_6.setObjectName("label_6")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_6.setFont(font)

        self.label_8 = QtWidgets.QLabel(self.mainWidget)
        self.label_8.setGeometry(QtCore.QRect(10, 360, 320, 20))
        self.label_8.setObjectName("label_8")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_8.setFont(font)

        # Save button
        self.save_settings = QtWidgets.QPushButton(self.mainWidget)
        self.save_settings.setGeometry(QtCore.QRect(572, 440, 121, 33))
        self.save_settings.setObjectName("save_settings")
        self.save_settings.clicked.connect(self.saveChangesToJson)

        # Discard button
        self.discard_changes = QtWidgets.QPushButton(self.mainWidget)
        self.discard_changes.setGeometry(QtCore.QRect(430, 440, 121, 33))
        self.discard_changes.setObjectName("discard_changes")
        self.discard_changes.clicked.connect(self.closeWindow)

        QtCore.QMetaObject.connectSlotsByName(self.mainWidget)
        self.setStyleSheet(
            """
            QWidget{
                background-color:#F7F7F7;
            }
            QPushButton#closeButn{
                border: 1px solid transparent;
                border-radius: 3px;
            }
            QPushButton#closeButn:hover{
                background-color:#d1d1d1;
            }
            QLineEdit{
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px 5px;
                height: 60px;
                font-size: 12px;
            }
            QComboBox{
                border: 2px solid #ccc;
                border-radius:5px;
                padding: 5px 5px;
            }
            QComboBox::down-arrow{
                image: url(./resources/arrow-down-12.png);
                border : none;
            }
            QComboBox::drop-down{
                border: none;
            }
            QPushButton#save_settings{
                font-size: 10pt;
                padding: 5px;
                border: 1px solid darkgray;
                border-radius: 7px;
                background-color: #2781F2;
                color: #ffffff;
            }
            QPushButton#discard_changes{
                font-size: 10pt;
                background: transparent;
                border: 1px solid #FF0000;
                border-radius: 7px;
                padding:5px;
            }
            QPushButton#save_settings:hover{
                background-color: #3185eb;
            }
            QPushButton#save_settings:pressed{
                background-color: #387cd1;
            }
            QPushButton#discard_changes:hover{
                background-color: #E81123;
                color: #fff;
            }
            QPushButton#discard_changes:pressed{
                background-color: #9B0B17;
            }
            QLabel#label_4, QLabel#label_5, QLabel#label_6, QLabel#label_8{
                color: #606770;
            }
            """)

    # Add drop-down menu to select default search engine
    def addDefaultSearchEngineSelector(self):
        self.searchEngineSelector = QtWidgets.QComboBox(self.mainWidget)
        self.searchEngineSelector.setEnabled(True)
        self.searchEngineSelector.setGeometry(QtCore.QRect(480, 80, 211, 33))

        # Search engines
        self.searchEngineSelector.addItem("Google")
        self.searchEngineSelector.addItem("Yahoo")
        self.searchEngineSelector.addItem("Bing")
        self.searchEngineSelector.addItem("DuckDuckGo")
        self.searchEngineSelector.currentTextChanged.connect(
            self.addDropDownItemToJson)

        if self.default_search_engine == "Google":
            self.searchEngineSelector.setCurrentIndex(0)
        elif self.default_search_engine == "Yahoo":
            self.searchEngineSelector.setCurrentIndex(1)
        elif self.default_search_engine == "Bing":
            self.searchEngineSelector.setCurrentIndex(2)
        elif self.default_search_engine == "DuckDuckGo":
            self.searchEngineSelector.setCurrentIndex(3)

    # Write to json

    def saveChangesToJson(self):  # startup pg
        if len(self.startup_page.text()) > 0:
            settings_data["startupPage"] = self.startup_page.text()
            with open("settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)

        if len(self.home_button_page.text()) > 0:
            settings_data["homeButtonPage"] = self.home_button_page.text()
            with open("settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)

        if len(self.new_tab_page.text()) > 0:
            settings_data["newTabPage"] = self.new_tab_page.text()
            with open("settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)

    def addDropDownItemToJson(self):
        settings_data["defaultSearchEngine"] = self.searchEngineSelector.currentText()
        with open("settings.json", "w") as f:
            json.dump(settings_data, f, indent=2)

    def closeWindow(self):
        self.close()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("Form", "Settings"))
        self.label_3.setText(_translate("Form", "On startup"))
        self.save_settings.setText(_translate("Form", "Save settings"))
        self.label.setText(_translate("Form", "Default Search Engine"))
        self.label_4.setText(_translate(
            "Form", "Choose what page to display on startup"))
        self.label_5.setText(_translate(
            "Form", "Default search engine used in the address bar"))
        self.label_6.setText(_translate(
            "Form", "Choose what page to navigate when home button is pressed"))
        self.label_7.setText(_translate("Form", "Home button"))
        self.label_8.setText(_translate(
            "Form", "Choose what page to show when a new tab is opened"))
        self.label_9.setText(_translate("Form", "New tab"))
        self.discard_changes.setText(_translate("Form", "Discard changes"))


class PrintHandler (QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_page = None
        self.m_inPrintPreview = False

    def setPage(self, page):
        assert not self.m_page
        self.m_page = page
        self.m_page.printRequested.connect(self.printPreview)

    @pyqtSlot()
    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self.m_page.view())
        if dialog.exec_() != QDialog.Accepted:
            return
        self.printDocument(printer)

    @pyqtSlot()
    def printPreview(self):
        if not self.m_page:
            return
        if self.m_inPrintPreview:
            return
        self.m_inPrintPreview = True
        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self.m_page.view())
        preview.paintRequested.connect(self.printDocument)
        preview.exec()
        self.m_inPrintPreview = False

    @pyqtSlot(QPrinter)
    def printDocument(self, printer):
        loop = QEventLoop()
        result = False

        def printPreview(success):
            nonlocal result
            result = success
            loop.quit()

        # progressbar to show loading
        progressbar = QProgressDialog(self.m_page.view())
        progressbar.findChild(QProgressBar).setTextVisible(False)
        progressbar.setLabelText("Please wait...")
        progressbar.setRange(0, 0)
        progressbar.show()
        progressbar.canceled.connect(loop.quit)
        self.m_page.print(printer, printPreview)
        loop.exec_()
        progressbar.close()

        if not result:
            painter = QPainter()
            if painter.begin(printer):
                font = painter.font()
                font.setPixelSize(20)
                painter.setFont(font)
                painter.drawText(
                    QPointF(10, 25), "We could not generate print preview.")
                painter.end()


class HistoryWindow (QWidget):
    def __init__(self):
        super().__init__()

        titleLbl = QLabel("History")
        titleLbl.setStyleSheet("""
            margin-top:7px;
        """)
        titleLbl.setFont(textFont)

        clearBtn = QPushButton("Clear")
        clearBtn.setObjectName("ClearButnHistory")
        clearBtn.setFont(textFont)
        clearBtn.setStyleSheet(
            """
            QPushButton#ClearButnHistory{
                border:1px solid transparent;
                border-radius: 7px;
                border-color:#ccc;
                margin-top:6px;
                margin-left:80px;
                margin-right:10px;
                padding: 5px 5px 5px 5px;
                font-size:12pt;
                color:#000;
                background-color:transparent;
            }

            QPushButton#ClearButnHistory:hover{
                background-color:#2681f2;
                border-color:#dae0e5;
                color: #fff;
            }

            QPushButton#ClearButnHistory:pressed{
                background-color:#0c63ce;
            }          
            """
        )
        clearBtn.clicked.connect(self.clearHistory)

        self.historyList = QListWidget()
        # self.historyList.horizontalScrollBar().setEnabled(False)
        self.historyList.horizontalScrollBar().setStyleSheet(
            """
                QScrollBar:horizontal {
                    height:8px;
                }
                QScrollBar::handle:horizontal {
                    background: gray;
                    min-height: 5px;
                    border: 1px solid gray;
                    border-radius: 4px;
                }
                QScrollBar::left-arrow:horizontal {
                    background:none;
                }
                QScrollBar::right-arrow:horizontal {
                    background:none;
                }
            """
        )
        self.historyList.verticalScrollBar().setStyleSheet(
            """
            QScrollBar:vertical {
                background: transparent;
                width:8px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: gray;
                min-width: 5px;
                border: 1px solid gray;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical{
                background:none;
            }
            QScrollBar::sub-line:vertical{
                background:none;
            }
        """
        )

        self.fillHistoryList()

        self.historyList.itemClicked.connect(self.goClickedLink)
        self.historyList.setStyleSheet(
            """
        QListWidget::item{
            padding-top: 8px;
            padding-bottom: 8px;
            margin-top: 2px;
            margin-bottom: 2px;
        }

        QListWidget::item:hover{
            background-color:#dce9ef;
        }
        
        QListWidget{
            border: 1px solid transparent;
            border-top: 1px solid gray;
            padding-left:5px;
            padding-right:5px;
        }
        """
        )

        layout = QGridLayout()

        layout.addWidget(titleLbl, 0, 0)
        layout.addWidget(clearBtn, 0, 1)
        layout.addWidget(self.historyList, 1, 0, 1, 2)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def fillHistoryList(self):
        data = cursor.execute("SELECT * FROM history")
        siteInfoList = data.fetchall()
        for i in range(len(siteInfoList) - 1, -1, -1):
            siteInfo = siteInfoList[i][1] + " - " + siteInfoList[i][3]
            self.historyList.addItem(siteInfo)

    def goClickedLink(self, item):
        siteName = item.text()
        visitDate = siteName[len(siteName) - 19:]
        siteInfoFromDB = cursor.execute(
            "SELECT * FROM history WHERE date = ?", [visitDate])
        try:
            url = siteInfoFromDB.fetchall()[0][2]
            w = mainWindow()
            w.openSiteHistoryClicked(QtCore.QUrl(
                url), str(siteName))  # open selected url
        except:
            self.close()

        self.close()

    def clearHistory(self):
        self.historyList.clear()
        cursor.execute("DELETE FROM history")
        connection.commit()


class AddressBar (QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFocus()

    def mousePressEvent(self, e):
        self.selectAll()

    def initAddressBar(self):
        # Set the placeholder text
        self.setPlaceholderText("Search or enter web address")

        # Set focus to the address bar
        self.setFocus()
        self.setStyleSheet("""
            QLineEdit{
                font-family: \"Segoe UI\";
                padding-top:4px;
                padding-left:8px;
                padding-bottom:4px;
                border:2px solid transparent;
                border-radius:6px;
                font-size:10pt;
                background-color: #ffffff;
                selection-background-color: #66c2ff;
            }

            QLineEdit:focus{
                border-color:#3696ff;
            }

            QLineEdit:hover{
                border-color:#d6d6d6
            }
            
        """)


class SSLIcon (QLabel):
    def __init__(self):
        super().__init__()
        self.InitSSLIcon()

    def InitSSLIcon(self):
        self.setObjectName("SSLIcon")
        self.setPixmap(QPixmap(os.path.join('resources', 'lock-icon.png')))


class Tabs (QTabWidget):
    def __init__(self):
        super().__init__()
        self.setDocumentMode(True)

        # Set the tabs closable
        self.setTabsClosable(True)

        # Set the tabs movable
        self.setMovable(True)
        # Add some styles to the tabs
        self.setStyleSheet("""
             QTabBar{
                background-color:#417294;
            }

            QTabBar::tab {
                background-color: none;
                color: #fff;
                padding: 6px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding-right:60px;
                max-width:80px;
            }

            QTabBar::tab:!selected{
                background-color: transparent;
            }

            QTabBar::tab:selected, QTabBar::tab:hover {     /* not selected tabs */
                background-color: #2c5470;
            }

            QTabBar::close-button {    /* style the tab close button */
                image: url(./resources/closetabbutton.png);
                subcontrol-position: right;
                border: 1px solid transparent;
                border-radius:3px;
            }

            QTabBar::close-button:hover{    /* close button hover */
                background-color: #477494
            }

            QTabWidget::tab-bar {
                left: 5px; /* move to the right by 5px */
            }

            QTabBar::tab:selected{  /* selected tabs */
                background-color: #00496e;
            }
        """)


class customWebEnginePage (QWebEnginePage):
    def createWindow(self, _type):
        page = customWebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @QtCore.pyqtSlot(QtCore.QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()


class AboutDialog (QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        butn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(butn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.setStyleSheet(
            """
            QPushButton{
                border:1px solid transparent;
                border-radius: 7px;
                border-color:#ccc;
                padding-top: 8px;
                padding-bottom: 8px;
                padding-right: 30px;
                padding-left: 30px;
                font-size:12pt;
                color:#fff;
                background-color:#0E71EB;
            }

            QPushButton:hover{
                background-color:#2681F2;
                border-color:#dae0e5;
                color: #fff;
            }

            QPushButton:pressed{
                background-color:#0C63CE;
            }          
            
        """)

        layout = QVBoxLayout()

        image = QLabel()
        browserIcon = QPixmap(os.path.join("Icons", "browser.png"))
        browserIcon = browserIcon.scaled(60, 60)
        image.setPixmap(browserIcon)

        hint = QLabel("About")
        hint.setStyleSheet("""
        font-size: 18px;
        margin-bottom: 10px;
        """)

        title = QLabel("Simple Web Browser")
        title.setStyleSheet(
            """margin-left:100px;
               font-size: 24px;
            """
        )
        title.setFont(textFont)

        layout2 = QHBoxLayout()
        layout2.addWidget(image)
        layout2.addWidget(title)
        layout.addWidget(hint)
        layout.addLayout(layout2)

        text1 = QLabel(
            "Learn more:\nhttps://github.com/saminsakur/PyQt5BrowserBuild")
        text1.setStyleSheet("""
            margin-top: 20px;
        """)

        text2 = QLabel("Made by Samin Sakur - https://github.com/saminsakur")
        text2.setStyleSheet("""
            margin-top: 20px;
        """)

        layout.addWidget(text1)
        layout.addWidget(text2)
        layout.addWidget(self.buttonBox)

        self.setStyleSheet(
            """QLabel{
            font-size: 12pt;
        }""")
        self.setWindowTitle("Simple web browser")
        self.setLayout(layout)


def main():
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

    try:
        sys.exit(app.exec_())

    except SystemExit:
        print("Closing browser...")


if __name__ == "__main__":
    main()
