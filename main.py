import os
import re
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


domains = (
    "com",
    "co",
    "net", 
    "org", 
    "io", 
    "in", 
    "me", 
    "app", 
    "gg", 
    "cc", 
    "bd", 
    "com.bd", 
    "google", 
    "in", 
    "us", 
    "uk", 
    "gov", 
    "int", 
    "edu", 
    "edu.bd", 
    "apple"
    "localhost"
)


class AboutDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        butn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(butn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self. buttonBox.setWhatsThis("Close The dialog")
        layout = QVBoxLayout()

        title = QLabel("Simple Browser")
        title.setWhatsThis("Simple Browser by Samin Sakur - https://github.com/saminsakur/PyQt5BrowserBuild")
        font = title.font()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        title.setFont(font)
        self.setWindowTitle("Simple web browser")

        layout.addWidget(title)
        layout.addWidget(QLabel("About:\nhttps://github.com/saminsakur/PyQt5BrowserBuild"))
        layout.addWidget(QLabel("Made by Samin Sakur - https://github.com/saminsakur"))
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)
        


class mainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__()

        # create tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Add some styles to the tabs
        self.tabs.setStyleSheet("""
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
            }

            QTabBar::tab:!selected{
                background-color: transparent;
            }
            

            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color:#005a87;
            }

            QTabBar::close-button {
                image: url(Images/closetabbutton.png);
                subcontrol-position: right;
            }

            QTabBar::close-button:hover{
                background-color:#a3a3a3;
            }

            QTabWidget::tab-bar {
                left: 5px;
            }
        """)
        # Add new tab when tab tab is doubleclicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # To connect to a function when currrent tab has been changed
        self.tabs.currentChanged.connect(self.tab_changed)

        # Set the tabs closable
        self.tabs.setTabsClosable(True)

        # Function to handle tab closing
        self.tabs.tabCloseRequested.connect(self.close_current_tab)


        # nav bar
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.addToolBar(self.navbar)

        # back button
        back_btn = QPushButton(self)
        back_btn.setObjectName("back_btn")
        back_btn.setIcon(QtGui.QIcon(os.path.join("Images", "left-arrow.png")))
        back_btn.setToolTip("Back to previous page")
        back_btn.clicked.connect(self.navigate_back_tab)
        self.navbar.addWidget(back_btn)

        # forward button
        forward_butn = QPushButton(self)       
        forward_butn.setObjectName("forward_butn")
        forward_butn.setIcon(QtGui.QIcon(os.path.join("Images", "right-arrow.png")))
        forward_butn.setToolTip("Go forward")
        forward_butn.clicked.connect(self.forward_tab)
        self.navbar.addWidget(forward_butn)

        # Refresh button
        self.reload_butn = QPushButton(self)
        self.reload_butn.setObjectName("reload_butn")
        self.reload_butn.setToolTip("Reload current page")
        self.reload_butn.resize(QSize(50, 20))
        self.reload_butn.setIcon(QtGui.QIcon(os.path.join("Images", "refresh.png")))
        self.reload_butn.clicked.connect(self.reload_tab)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setObjectName("stop_butn")
        self.stop_btn.setToolTip("Stop loading current page")
        self.stop_btn.setIcon(QIcon(os.path.join('Images', 'cross.png')))
        self.stop_btn.clicked.connect(self.stop_loading_tab)

        # Added stop button 
        self.stop_action = self.navbar.addWidget(self.stop_btn)

        # Added reload button
        self.reload_action = self.navbar.addWidget(self.reload_butn)

        # Home button
        self.home_button = QPushButton(self)
        self.home_button.setObjectName("home_button")
        self.home_button.setToolTip("Back to home")
        self.home_button.setIcon(QtGui.QIcon(os.path.join("Images", "home.png")))
        self.home_button.clicked.connect(self.goToHome)
        self.navbar.addWidget(self.home_button)

        
        # Add Address bar
        self.url_bar = QLineEdit()
        self.url_bar.setFrame(False)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setToolTip(self.url_bar.text())

        # Set the placeholder text
        self.url_bar.setPlaceholderText("Search or enter web address")
        self.url_bar.setFocus()
        self.url_bar.setStyleSheet("""
            QLineEdit{
                font-family: Segoe UI;
                padding-top:4px;
                padding-left:8px;
                padding-bottom:4px;
                border:2px solid transparent;
                border-radius:6px;
                font-size:10pt;
                background-color: #ffffff;
            }

            QLineEdit:focus{
                border-color:#00aee3;
            }

            QLineEdit:hover{
                border-color:#d6d6d6
            }
        """)

        # Set stop action to be invisible
        self.stop_action.setVisible(False)

        # Add a separator
        self.navbar.addSeparator()

        # Shows ssl security icon
        self.httpsicon = QLabel()
        self.httpsicon.setObjectName("SSLIcon")
        self.httpsicon.setPixmap(QPixmap(os.path.join('Images', 'lock-icon.png')))

        # Add http icon to the navbar bar
        self.navbar.addWidget(self.httpsicon)

        # Add Address Bar to the navbar
        self.navbar.addWidget(self.url_bar)

        # The conetext menu
        context_menu = QMenu(self)
        
        # Button for the three dot context menu button
        ContextMenuButton = QPushButton(self)
        ContextMenuButton.setObjectName("ContextMenuButton")

        # Give the three dot image to the Qpush button
        ContextMenuButton.setIcon(QIcon(os.path.join("Images", "more.png")))    # Add icon
        ContextMenuButton.setObjectName("ContextMenuTriggerButn")
        ContextMenuButton.setToolTip("More")

        # Add the context menu to the three dot context menu button
        ContextMenuButton.setMenu(context_menu)

        """Actions of the three dot context menu"""

        # Add new tab
        newTabAction = QAction("New tab", self)
        newTabAction.setIcon(QtGui.QIcon(os.path.join("Images", "newtab.png")))
        newTabAction.triggered.connect(lambda: self.add_new_tab(QUrl("https://www.google.com/"), "Homepage"))
        newTabAction.setToolTip("Add a new tab")
        context_menu.addAction(newTabAction)

        # Close tab action
        CloseTabAction = QAction("Close tab", self)
        CloseTabAction.setIcon(QIcon(os.path.join("Images", "closetab.png")))
        CloseTabAction.triggered.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))
        context_menu.addAction(CloseTabAction)

        # A separator
        context_menu.addSeparator()

        # Feature to navigate to bing
        GoToBingAction = QAction("Bing", self)
        GoToBingAction.setIcon(QIcon(os.path.join("Images", "globe.png")))
        GoToBingAction.triggered.connect(self.GoToBing)
        context_menu.addAction(GoToBingAction)

        # Feature to navigate to DuckDuckGo
        GoToDuckDuckGo = QAction(QIcon(os.path.join("Images", "globe.png")), "DuckDuckgo", self)
        GoToDuckDuckGo.triggered.connect(self.NavigateDuckDuckGo)
        context_menu.addAction(GoToDuckDuckGo)

        # Another separator
        context_menu.addSeparator()

        # Feature to copy site url
        CopySiteAddress = QAction(QtGui.QIcon(os.path.join("Images", "url.png")), "Copy site url", self)
        CopySiteAddress.triggered.connect(self.CopySiteLink)
        context_menu.addAction(CopySiteAddress)

        # Fetaure to go to copied site url
        PasteAndGo = QAction(QtGui.QIcon(os.path.join("Images", "paste.png")), "Paste and go", self)
        PasteAndGo.triggered.connect(self.PasteUrlAndGo)
        context_menu.addAction(PasteAndGo)

        # Open page
        OpenPgAction = QAction("Open", self)
        OpenPgAction.setIcon(QtGui.QIcon(os.path.join("Images", "openclickhtml.png")))
        context_menu.addAction(OpenPgAction)

        # Save page as
        SavePageAs = QAction("Save page as", self)
        SavePageAs.setIcon(QtGui.QIcon(os.path.join("Images", "save-disk.png")))
        context_menu.addAction(SavePageAs)

        # Print this page action
        PrintThisPageAction = QAction("Print this page", self)
        PrintThisPageAction.setIcon(QtGui.QIcon(os.path.join("Images", "printer.png")))
        context_menu.addAction(PrintThisPageAction)

        # The help submenu
        HelpMenu = QMenu("Help", self)
        HelpMenu.setIcon(QIcon(os.path.join("Images", "question.png")))

        # About action
        AboutAction = QAction("About this browser", self)
        AboutAction.setIcon(QIcon(os.path.join("Images", "info.png")))
        AboutAction.triggered.connect(self.about)
        HelpMenu.addAction(AboutAction)

        context_menu.addMenu(HelpMenu)

        # Add a separator
        context_menu.addSeparator()



        # Close browser
        CloseBrowser = QAction("Close browser", self)
        CloseBrowser.triggered.connect(lambda: sys.exit())
        context_menu.addAction(CloseBrowser)


        # Set menu for the button
        # ContextMenuButton.add
        # Add the context menu to the navbar
        self.navbar.addWidget(ContextMenuButton)
        
        # Stuffs to see at starup
        self.add_new_tab(QUrl("https://www.google.com/"), "Homepage")

        # what to display on the window
        self.setCentralWidget(self.tabs)

        # Stuffs to set the window
        self.showMaximized()
    
    """Instead of managing 2 slots associated with the progress and completion of loading,
        only one of them should be used since, for example, the associated slot is also 
        called when it is loaded at 100% so it could be hidden since it can be invoked together with finished."""
    @QtCore.pyqtSlot(int)
    def loadProgressHandler(self, prog):
        if self.tabs.currentWidget() is not self.sender():
            return

        loading = prog < 100

        self.stop_action.setVisible(loading)
        self.reload_action.setVisible(not loading)
        pass



    # funcion to navigate to home whaen home icon is pressed   
    def goToHome(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com/"))

    # Function to navigate to bing by pressing go to bing on the three dot menu
    def GoToBing(self):
        self.add_new_tab(QUrl("https://www.bing.com/"), "Bing")

    # Function to navigate DuckDuckGo
    def NavigateDuckDuckGo(self):
        self.add_new_tab(QtCore.QUrl("https://www.duckduckgo.com/"), "DuckDuckGo")

    def CopySiteLink(self):
        # print(QGuiApplication.clipboard())
        pass

    def PasteUrlAndGo(self):
        # print(self.tabs.currentWidget().clipboard())
        pass

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

    # doubleclick on empty space for new tab
    def tab_open_doubleclick(self, i):
        if i == -1: # No tab under the click
            self.add_new_tab(QUrl("http://www.google.com/"), label="New tab")
    
    # to update the tab
    def tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    # to close current tab
    def close_current_tab(self, i):
        if self.tabs.count() < 2 :
            return

        self.tabs.removeTab(i)
    
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("{} Simple Web Browser".format(title))

    # To close current tab
    def close_tab(self, i):
        self.tabs.removeTab(i)
    
    # function to add new tab
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('https://www.google.com/')
        
        browser = QWebEngineView()  # Define the main webview to browser the internet

        browser.loadProgress.connect(self.loadProgressHandler)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.load(qurl)

        # update url when it's from the correct tab
        # update url when it's from the correct tab
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def select_all_text(self):
        self.url_bar.selectAll()

    def about(self):
        dialouge = AboutDialog()
        dialouge.exec_()

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            # if signal is not from the current tab, then ignore
            return
        
        if q.scheme() == 'https':
            # secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "security.png")))
            self.httpsicon.setToolTip("Connection to this is is secure\n\nThis site have a valid certificate")
        
        elif q.scheme() == "file:":
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "file-protocol.png")))
        else:
            # Set insecure padlock
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "warning1.png")))
            self.httpsicon.setToolTip("Connection to this site may not be secured")


        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    # function to search google from the search box
    def searchGoogle(self, text): 
        if not len(text) <= 0:
            return "https://www.google.com/search?q="+"+".join(text.split())

    """
    function to navigate to url, if the url ends with the domains from the domains tuple,
    then "http://" will be added after what the user have written if not, then it will call
    the searchGoogle() function to search google directly from the search box
    """
    def navigate_to_url(self):
        in_url = self.url_bar.text()
        url = ""
        """ if the text in the search box endswith one of the domain in the domains tuple, then "http://" will be added
         if the text is pre "http://" or "https://" added, then not"""               
        # [0-9A-Za-z]+\.+[A-Za-z0-9]{2}

        if self.tabs.currentWidget is None: # To avoid exception
            # If QTabWidget's currentwidet is none, the ignore
            return

        if QUrl(in_url).scheme() == "file":
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.tabs.currentWidget().load(local_url)
            

        elif any([in_url.endswith(domains), in_url.endswith("/")]) and not any(i in in_url  for i in ("http://","https://","file:///")):
            url = "http://"+in_url

        # this will search google
        elif not any(i in in_url for i in domains) or not any(i in in_url  for i in("http:", "https:", "/")):
            url = self.searchGoogle(in_url)
                
        # else browser will go to anything the user has been written
        else:
            url = in_url

        
        self.tabs.currentWidget().load(QUrl.fromUserInput(url))




def main():
    app = QApplication(sys.argv)

    # Set the window name
    QApplication.setApplicationName("Simple Web Browser")

    # Set the window icon
    QApplication.setWindowIcon(QIcon(os.path.join("Images", "browser.png")))

    # App styles
    app.setStyleSheet("""
    QPushButton#ContextMenuTriggerButn::menu-indicator{ /* Hide context menu button dropdown icon */
        image: none;
    }

    QToolBar {
        background-color: #edf2fb;
    }

    /*
     The three dot menu 
    */

    QMenu {
        background-color: #fafaf6;
        border: 1px solid transparent;
        padding:10px;
        padding-left:10px;
        padding-right:10px;
    }

    QMenu::item {
        background-color: transparent;
        padding-left:70px;
        padding-right:70px;
        padding-top:6px;
        padding-bottom:6px;
        font-family: fantasy;
        font-size:9pt;
        height:25px;
        width:80px;
    }

    QMenu::separator {
        height: 2px;
        background: #111;
        margin-left: 0%;
        margin-right: 0%;
    }
    QMenu::item:selected{
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
        border-radius:10px;
        padding:5px;
        border-width:2px;
        border-style:solid;
        border-radius:20px;
        border: 2px solid transparent;
    }

    QLabel#SSLIcon {    /* ssl icon */
        border: 1px solid transparent;
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 6px;
        width: 5px;
        height: 5px;
    }

    QLabel#SSLIcon:hover {  /* ssl icon on hover */
        background-color: #d1d8eb;
    }

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
        background-color: #d1d8eb;
    }

    QPushButton#back_btn:hover {
        background-color: #d1d8eb;
    }

    QPushButton#forward_butn:hover {
        background-color: #d1d8eb;
    }

    QPushButton#reload_butn:hover {
        background-color: #d1d8eb;
    }

    QPushButton#home_button:hover {
        background-color: #d1d8eb;
    }

    QPushButton#ContextMenuTriggerButn:hover {
        background-color: #d1d8eb;
    }

    /*
    * after pressed
    */

    QPushButton#stop_butn:pressed {
        background-color: #ccd1db;
    }

    QPushButton#back_btn:pressed {
        background-color: #ccd1db;
    }

    QPushButton#forward_butn:pressed {
        background-color: #ccd1db;
    }

    QPushButton#reload_butn:pressed {
        background-color: #ccd1db;
    }

    QPushButton#home_button:pressed {
        background-color: #ccd1db;
    }

    QPushButton#ContextMenuTriggerButn:pressed {
        background-color: #ccd1db;
    }

    """)

    #e6e6e6 background color
    window = mainWindow()
    app.exec_()



if __name__ == "__main__":
    main()







