from PyQt5.QtWebEngineWidgets import (
    QWebEngineDownloadItem,
    QWebEngineSettings,
    QWebEngineView,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QShortcut,
    QToolBar,
    QMenu,
    QAction,
    QFileDialog,
)
from PyQt5.QtCore import QSize, QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
import browser.widgets
import browser.printer
import browser.errors
import browser.about
import browser.history
import browser.settings
import browser
import sys
import os
import re
import pyperclip as pc
import datetime


# Regular expressions to match urls
pattern = re.compile(
    r"^(http|https)?:?(\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)
without_http_pattern = re.compile(
    r"[\-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)
file_pattern = re.compile(r"^file://")


class mainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.tabs = browser.widgets.Tabs()  # create tabs

        # create history table
        browser.cursor.execute(
            """CREATE TABLE IF NOT EXISTS "history" (
                "id"	INTEGER,
                "title"	TEXT,
                "url"	TEXT,
                "date"	TEXT,
                PRIMARY KEY("id")
            )"""
        )

        # Add new tab when tab tab is doubleclicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # To connect to a function when current tab has been changed
        self.tabs.currentChanged.connect(self.tab_changed)

        # Function to handle tab closing
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # open new tab when Ctrl+T pressed
        AddNewTabKeyShortcut = QShortcut("Ctrl+T", self)
        AddNewTabKeyShortcut.activated.connect(
            lambda: self.add_new_tab(
                QtCore.QUrl(browser.settings_data["newTabPage"], "New tab")
            )
        )

        # Close current tab on Ctrl+W
        CloseCurrentTabKeyShortcut = QShortcut("Ctrl+W", self)
        CloseCurrentTabKeyShortcut.activated.connect(
            lambda: self.close_current_tab(self.tabs.currentIndex())
        )

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
        back_btn.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "left-arrow.png"))
        )
        back_btn.setToolTip("Back to previous page")
        back_btn.setShortcut("Alt+Left")
        back_btn.clicked.connect(self.navigate_back_tab)
        self.navbar.addWidget(back_btn)

        # forward button
        forward_butn = QPushButton(self)
        forward_butn.setObjectName("forward_butn")
        forward_butn.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "right-arrow.png"))
        )
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
        self.reload_butn.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "refresh.png"))
        )
        self.reload_butn.clicked.connect(self.reload_tab)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setObjectName("stop_butn")
        self.stop_btn.setToolTip("Stop loading current page")
        self.stop_btn.setShortcut("Escape")
        self.stop_btn.setIcon(QIcon(os.path.join("resources", "icons", "cross.png")))
        self.stop_btn.clicked.connect(self.stop_loading_tab)

        # Added stop button
        self.stop_action = self.navbar.addWidget(self.stop_btn)

        # Added reload button
        self.reload_action = self.navbar.addWidget(self.reload_butn)

        # Home button
        self.home_button = QPushButton(self)
        self.home_button.setObjectName("home_button")
        self.home_button.setToolTip("Back to home")
        self.home_button.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "home.png"))
        )
        self.home_button.clicked.connect(self.goToHome)
        self.navbar.addWidget(self.home_button)

        # Add Address bar
        self.url_bar = browser.widgets.AddressBar()
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
        self.httpsicon = browser.widgets.SSLIcon()

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
            QIcon(os.path.join("resources", "icons", "more.png"))
        )  # Add icon
        ContextMenuButton.setObjectName("ContextMenuTriggerButn")
        ContextMenuButton.setToolTip("More")

        # Add the context menu to the three dot context menu button
        ContextMenuButton.setMenu(context_menu)

        """Actions of the three dot context menu"""

        # Add new tab
        newTabAction = QAction("New tab", self)
        newTabAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "newtab.png"))
        )
        newTabAction.triggered.connect(
            lambda: self.add_new_tab(
                QUrl(browser.settings_data["newTabPage"]), "Homepage"
            )
        )
        newTabAction.setToolTip("Add a new tab")
        context_menu.addAction(newTabAction)

        # New window action
        newWindowAction = QAction("New window", self)
        newWindowAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "app_window_ios.png"))
        )
        newWindowAction.triggered.connect(self.CreateNewWindow)
        context_menu.addAction(newWindowAction)

        # Close tab action
        CloseTabAction = QAction("Close tab", self)
        CloseTabAction.setIcon(
            QIcon(os.path.join("resources", "icons", "closetab.png"))
        )
        CloseTabAction.triggered.connect(
            lambda: self.close_current_tab(self.tabs.currentIndex())
        )
        CloseTabAction.setToolTip("Close current tab")
        context_menu.addAction(CloseTabAction)

        # A separator
        context_menu.addSeparator()

        # Another separator
        context_menu.addSeparator()

        # Feature to copy site url
        CopySiteAddress = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "url.png")),
            "Copy site url",
            self,
        )
        CopySiteAddress.triggered.connect(self.CopySiteLink)
        CopySiteAddress.setToolTip("Copy current site address")
        context_menu.addAction(CopySiteAddress)

        # Fetaure to go to copied site url
        PasteAndGo = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "paste.png")),
            "Paste and go",
            self,
        )
        PasteAndGo.triggered.connect(self.PasteUrlAndGo)
        PasteAndGo.setToolTip("Go to the an url copied to your clipboard")
        context_menu.addAction(PasteAndGo)

        # A separator
        context_menu.addSeparator()

        # View history
        ViewHistory = QAction("History", self)
        ViewHistory.setIcon(QIcon(os.path.join("resources", "icons", "history.png")))
        ViewHistory.triggered.connect(self.openHistory)
        ViewHistory.setShortcut("Ctrl+h")
        context_menu.addAction(ViewHistory)

        # Open page
        OpenPgAction = QAction("Open", self)
        OpenPgAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "openclickhtml.png"))
        )
        OpenPgAction.setToolTip("Open a file in this browser")
        OpenPgAction.setShortcut("Ctrl+O")
        OpenPgAction.triggered.connect(self.open_local_file)
        context_menu.addAction(OpenPgAction)

        # Save page as
        SavePageAs = QAction("Save page as", self)
        SavePageAs.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "save-disk.png"))
        )
        SavePageAs.setToolTip("Save current page to this device")
        SavePageAs.setShortcut("Ctrl+S")
        SavePageAs.triggered.connect(self.save_page)
        context_menu.addAction(SavePageAs)

        # Print this page action
        PrintThisPageAction = QAction("Print this page", self)
        PrintThisPageAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "printer.png"))
        )
        PrintThisPageAction.triggered.connect(self.print_this_page)
        PrintThisPageAction.setShortcut("Ctrl+P")
        PrintThisPageAction.setToolTip("Print current page")
        context_menu.addAction(PrintThisPageAction)

        # Print with preview
        PrintPageWithPreview = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "printerprev.png")),
            "Print page with preview",
            self,
        )
        PrintPageWithPreview.triggered.connect(self.PrintWithPreview)
        PrintPageWithPreview.setShortcut("Ctrl+Shift+P")
        context_menu.addAction(PrintPageWithPreview)

        # Save page as PDF
        SavePageAsPDF = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "adobepdf.png")),
            "Save as PDF",
            self,
        )
        SavePageAsPDF.triggered.connect(self.save_as_pdf)
        context_menu.addAction(SavePageAsPDF)

        context_menu.addSeparator()

        # Settings widget:
        userSettingsAction = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "settings.png")),
            "Settings",
            self,
        )
        userSettingsAction.triggered.connect(self.openSettings)
        context_menu.addAction(userSettingsAction)

        # The help submenu
        HelpMenu = QMenu("Help", self)
        HelpMenu.setObjectName("HelpMenu")
        HelpMenu.setIcon(QIcon(os.path.join("resources", "icons", "question.png")))

        # About action
        AboutAction = QAction("About this browser", self)
        AboutAction.setIcon(QIcon(os.path.join("resources", "icons", "info.png")))
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
        self.add_new_tab(QUrl(browser.settings_data["startupPage"]), "Homepage")

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
        self.tabs.currentWidget().setUrl(QUrl(browser.settings_data["homeButtonPage"]))

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
            QUrl("https://github.com/saminsakur/PyQt5BrowserBuild"), "Github"
        )

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
            filter="Hypertext Markup Language (*.htm *.html *.mhtml);;All files (*.*)",
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf8") as f:
                    opened_file = f.read()
                    self.tabs.currentWidget().setHtml(opened_file)

            except:
                dlg = browser.errors.fileErrorDialog()
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
                    filepath, format=QWebEngineDownloadItem.MimeHtmlSaveFormat
                )

            elif filter == "Webpage, complete (*.htm *.html)":
                self.tabs.currentWidget().page().save(
                    filepath, format=QWebEngineDownloadItem.CompleteHtmlSaveFormat
                )

        except:
            self.showErrorDlg()

    # Print handler
    def print_this_page(self):
        try:
            handler_print = browser.printer.PrintHandler()
            handler_print.setPage(self.tabs.currentWidget().page())
            handler_print.print()

        except:
            self.showErrorDlg()

    # Print page with preview
    def PrintWithPreview(self):
        handler = browser.printer.PrintHandler()
        handler.setPage(self.tabs.currentWidget().page())
        handler.printPreview()

    # Save as pdf
    def save_as_pdf(self):
        filename, filter = QFileDialog.getSaveFileName(
            parent=self, caption="Save as", filter="PDF File (*.pdf);;All files (*.*)"
        )

        self.tabs.currentWidget().page().printToPdf(filename)

    # doubleclick on empty space for new tab
    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab(QUrl(browser.settings_data["newTabPage"]), label="New tab")

    # to update the tab
    def tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    # to close current tab
    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            self.close()

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

    # function to add new tab
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl(browser.settings_data["newTabPage"])

        _browser = QWebEngineView()  # Define the main webview to browser the internet

        # Set page
        _browser.setPage(browser.widgets.customWebEnginePage(_browser))

        # Full screen enable
        _browser.settings().setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True
        )
        _browser.page().fullScreenRequested.connect(lambda request: request.accept())

        _browser.loadProgress.connect(self.loadProgressHandler)

        _browser.page().WebAction()

        _browser.settings().setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)

        i = self.tabs.addTab(_browser, label)
        self.tabs.setCurrentIndex(i)

        _browser.load(qurl)
        self.url_bar.setFocus()

        # update url when it's from the correct tab
        _browser.urlChanged.connect(
            lambda qurl, browser=_browser: self.update_urlbar(qurl, browser)
        )

        _browser.loadFinished.connect(
            lambda _, i=i, browser=_browser: self.tabs.setTabText(
                i, browser.page().title()
            )
        )

        # update history when loading finished
        _browser.page().loadFinished.connect(self.updateHistory)

    def showErrorDlg(self):
        dlg = browser.errors.errorMsg()
        dlg.exec_()

    def about(self):
        self.AboutDialogue = browser.about.AboutDialog()
        self.AboutDialogue.show()

    # Update address bar to show current pages's url
    def update_urlbar(self, q, _browser=None):
        if _browser != self.tabs.currentWidget():
            # if signal is not from the current tab, then ignore
            return

            self.url_bar.clear()

        if q.toString() == browser.settings_data["newTabPage"]:
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("resources", "icons", "info_24.png"))
            )
            self.httpsicon.setToolTip("This is browser's new tab page")

        else:
            if q.scheme() == "https":
                # secure padlock icon
                self.httpsicon.setPixmap(
                    QPixmap(os.path.join("resources", "icons", "security.png"))
                )
                self.httpsicon.setToolTip(
                    "Connection to this is is secure\n\nThis site have a valid certificate"
                )

            elif q.scheme() == "file":
                self.httpsicon.setPixmap(
                    QPixmap(os.path.join("resources", "icons", "info_24.png"))
                )
                self.httpsicon.setToolTip("You are viewing a local or shared file")

            elif q.scheme() == "data":
                self.httpsicon.setPixmap(
                    QPixmap(os.path.join("resources", "icons", "info_24.png"))
                )
                self.httpsicon.setToolTip("You are viewing a local or shared file")

            else:
                # Set insecure padlock
                self.httpsicon.setPixmap(
                    QPixmap(os.path.join("resources", "icons", "warning.png"))
                )
                self.httpsicon.setToolTip("Connection to this site may not be secured")

        if q.toString() == browser.settings_data["newTabPage"]:
            self.url_bar.clear()
        else:
            self.url_bar.setText(q.toString())

        self.url_bar.setCursorPosition(0)

    # function to search google from the search box
    def searchWeb(self, text):
        Engine = browser.settings_data["defaultSearchEngine"]
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
        if len(str(in_url)) < 1:
            return

        if self.tabs.currentWidget is None:  # To avoid exception
            # If QTabWidget's currentwidget is none, the ignore
            return

        if file_pattern.search(in_url):
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.tabs.currentWidget().load(local_url)

        elif without_http_pattern.search(in_url) and any(
            [i in in_url for i in ["http://", "https://"]]
        ):
            url = in_url

        elif pattern.search(in_url) and not any(
            i in in_url for i in ("http://", "https://", "file:///")
        ):
            url = "http://" + in_url

        # this will search google
        elif not "/" in in_url:
            url = self.searchWeb(in_url)

        self.tabs.currentWidget().load(QUrl.fromUserInput(url))

    def updateHistory(self):
        title = self.tabs.currentWidget().page().title()
        url = str(self.tabs.currentWidget().page().url())
        url = url[19 : len(url) - 2]
        hour = datetime.datetime.now().strftime("%X")
        day = datetime.datetime.now().strftime("%x")
        date = hour + " - " + day

        data = browser.cursor.execute("SELECT * FROM history")
        siteInfoList = data.fetchall()

        for i in range(len(siteInfoList)):
            if url == siteInfoList[i][2]:
                browser.cursor.execute("DELETE FROM history WHERE url = ?", [url])

        browser.cursor.execute(
            "INSERT INTO history (title,url,date) VALUES (:title,:url,:date)",
            {"title": title, "url": url, "date": date},
        )

        browser.connection.commit()

    def openHistory(self):
        self.historyWindow = browser.history.HistoryWindow()
        self.historyWindow.setWindowFlags(Qt.Popup)
        self.historyWindow.setGeometry(
            int(self.tabs.currentWidget().frameGeometry().width() / 2 + 400),
            70,
            300,
            500,
        )
        self.historyWindow.setContentsMargins(0, 0, 0, 0)
        self.historyWindow.setStyleSheet(
            """
            background-color:#edf4f7;
            """
        )
        self.historyWindow.show()

    def openSiteHistoryClicked(self, url, *args):
        self.tabs.currentWidget().load(url)

    def openSettings(self):
        self.userSettingswindow = browser.settings.UserSettings()
        self.userSettingswindow.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)
        self.userSettingswindow.show()

    def closeEvent(self, a0):
        sys.exit()