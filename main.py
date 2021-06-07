import os
import sys
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.sip import *


domains = (
    "com", "net", "org", "io", "in", "me", "app", "gg", "cc", "bd", "com.bd", "google", "in", "us", "uk", "gov", "int", "edu", "edu.bd", "apple"
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
        self.tabs.tabBarDoubleClicked.connect( self.tab_open_doubleclick )
        self.tabs.currentChanged.connect(self.tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setStyleSheet("""
            background-color:#cfcfcf;
        """)
        self.setCentralWidget(self.tabs)

        # self.setCentralWidget(self.browser)
        self.showMaximized()


        # nav bar
        navbar = QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)

        # back button
        back_btn = QAction("Back", self)
        back_btn.setIcon(QtGui.QIcon(os.path.join("Images", "left-arrow.png")))
        back_btn.triggered.connect(self.navigate_back_tab)
        back_btn.setStyleSheet("""padding-right:5px;padding-left:5px;""")
        navbar.addAction(back_btn)

        # forward button
        forward_butn = QAction("Forward", self)
        forward_butn.setIcon(QtGui.QIcon(os.path.join("Images", "right-arrow.png")))
        forward_butn.triggered.connect(self.forward_tab)
        forward_butn.setStyleSheet("""padding-right:5px;padding-left:5px;""")
        navbar.addAction(forward_butn)

        # Refresh button
        reload_butn = QAction("Reload", self)
        reload_butn.setIcon(QtGui.QIcon(os.path.join("Images", "refresh.png")))
        reload_butn.triggered.connect(self.reload_tab)
        reload_butn.setStyleSheet("""padding-right:5px;padding-left:5px;""")
        navbar.addAction(reload_butn)

        # Home button
        home_button = QAction("Home", self)
        home_button.setIcon(QtGui.QIcon(os.path.join("Images", "home.png")))
        home_button.triggered.connect(self.goToHome)
        home_button.setStyleSheet("""padding-right:5px;padding-left:5px;""")
        navbar.addAction(home_button)
        
        navbar.addSeparator()

        # Shows ssl security icon
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('Images', 'lock-icon.png')))
        self.httpsicon.setStyleSheet("""padding-right:5px;padding-left:5px;""")
        navbar.addWidget(self.httpsicon)

        # Add search box
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            font-family: Arial;
            padding-top:4px;
            padding-left:8px;
            padding-bottom:4px;
            border:2px solid #bdbdbd;
            border-radius:6px;
            font-size:10pt;
        """)
        navbar.addWidget(self.url_bar)
        
        # Stop button
        stop_btn = QAction(QIcon(os.path.join('Images', 'cross.png')), "Stop Loading current page", self)
        stop_btn.triggered.connect(self.stop_loading_tab)
        navbar.addAction(stop_btn)
        
        # tab_close_button = QPushButton("Close tab", self)
        # tab_close_button.setStyleSheet('''color:red;''')
        # tab_close_button.pressed.connect(self.close_current_tab)
        # self.tabs.addAction(tab_close_button)
        navbar.addSeparator()

        aboutAction = QAction("About", self)
        aboutAction.setIcon(QIcon(os.path.join("Images", "info.png")))
        aboutAction.triggered.connect(self.about)
        navbar.addAction(aboutAction)

        

        # on startup
        self.add_new_tab(QUrl("https://www.google.com/"), "Homepage")
        self.show()
        
    # funcion to navigate to home whaen home icon is pressed   
    def goToHome(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com/"))

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

        elif self.tabs.count() == 0:
            sys.exit()

        self.tabs.removeTab(i)
    
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s Simple Web Browser" % title)

    # To close current tab
    def close_tab(self, i):
        self.tabs.removeTab(i)

    # function to add new tab
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl(' ')
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        # update url when it's from the correct tab
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
    
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
        
        else:
            # Set insecure padlock
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "warning1.png")))
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
        # if the text in the search box endswith one of the domain in the domains tuple, then "http://" will be added
        # if the text is pre "http://" or "https://" added, then not               
        # To open files
        
        if QUrl(in_url).scheme() == "file":
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.tabs.currentWidget().load(local_url)
            

        elif any([in_url.endswith(domains), in_url.endswith("/")]) and not any([in_url.startswith("http://"), in_url.startswith("https://"), in_url.startswith("file:///")]):
            url = "http://"+in_url

        # this will search google
        elif not in_url.endswith("/"):
            url = self.searchGoogle(in_url)
                
        # else browser will go to anything the user has been written
        else:
            url = in_url

        
        self.tabs.currentWidget().setUrl(QUrl(url))



app = QApplication(sys.argv)
QApplication.setApplicationName("Simple Web Browser")
QApplication.setWindowIcon(QIcon(os.path.join("Images", "browser.png")))
window = mainWindow()
app.exec_()
