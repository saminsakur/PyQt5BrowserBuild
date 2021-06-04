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
        self.setCentralWidget(self.tabs)

        # self.setCentralWidget(self.browser)
        self.showMaximized()


        # nav bar
        navbar = QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)

        # back button
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to the previous page")
        back_btn.setIcon(QtGui.QIcon(os.path.join("Images", "left-arrow.png")))
        back_btn.triggered.connect(self.navigate_back_tab)
        navbar.addAction(back_btn)

        # forward button
        forward_butn = QAction("Forward", self)
        forward_butn.setStatusTip("Forward to next page")
        forward_butn.setIcon(QtGui.QIcon(os.path.join("Images", "right-arrow.png")))
        forward_butn.triggered.connect(self.forward_tab)
        navbar.addAction(forward_butn)

        # Refresh button
        reload_butn = QAction("Reload", self)
        reload_butn.setStatusTip("Reload current page")
        reload_butn.setIcon(QtGui.QIcon(os.path.join("Images", "refresh2.png")))
        reload_butn.triggered.connect(self.reload_tab)
        navbar.addAction(reload_butn)

        # Home button
        home_button = QAction("Home", self)
        home_button.setIcon(QtGui.QIcon(os.path.join("Images", "home.png")))
        home_button.setStatusTip("Go home")
        home_button.triggered.connect(self.goToHome)
        navbar.addAction(home_button)
        
        navbar.addSeparator()

        # Shows ssl security icon
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('Images', 'lock-icon.png')))
        navbar.addWidget(self.httpsicon)

        # Add search box
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        # Stop button
        stop_btn = QAction(QIcon(os.path.join('Images', 'cross.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.stop_loading_tab)
        navbar.addAction(stop_btn)
        
        tab_close_button = QAction("Close tab", self)
        tab_close_button.triggered.connect(lambda: self.close_current_tab(self.tabs.currentIndex))
        navbar.addAction(tab_close_button)
        

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


        self.tabs.removeTab(i)
    
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s Simple Web Browser" % title)

    # To lose current tab
    def close_current_tab(self, i):
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
    
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            # if signal is not from the current tab, then ignore
            return
        
        if q.scheme() == 'https':
            # secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "security.png")))
        
        else:
            # Set insecure padlock
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "warning.png")))

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
        if any([in_url.endswith(domains), in_url.endswith("/")]) and not any([in_url.startswith("http://"), in_url.startswith("https://"), in_url.startswith("file:///")]):
            url = "http://"+in_url
        
        # To open files
        elif in_url.startswith("file:///"):
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.browser.load(local_url)

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
