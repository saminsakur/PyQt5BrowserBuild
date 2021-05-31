import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
domains = (".com", ".net", ".org", ".io", "in", "me", "app", "gg", "cc", "bd", "com.bd")


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com/"))
        self.setCentralWidget(self.browser)
        self.showMaximized()


        # nav bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        #back button
        back_btn = QAction(self)
        back_btn.setIcon(QtGui.QIcon("Images\\left-arrow.png"))
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # forward button
        forward_butn = QAction(self)
        forward_butn.setIcon(QtGui.QIcon("Images\\right-arrow.png"))
        forward_butn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_butn)

        # Refresh button
        reload_butn = QAction(self)
        reload_butn.setIcon(QtGui.QIcon("Images\\refresh2.png"))
        reload_butn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_butn)

        # Home button
        home_button = QAction(self)
        home_button.setIcon(QtGui.QIcon("Images\\home2.png"))
        home_button.triggered.connect(self.goToHome)
        navbar.addAction(home_button)
                
        # Add search box
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.updateUrl)
        
       
    def goToHome(self):
        self.browser.setUrl(QUrl('https://www.google.com/'))
    
    def navigate_to_url(self):
        in_url = self.url_bar.text()
        url = ""
        if in_url.endswith(domains) and "http://" not in url:
            url += "http://"+in_url

        else :
            url = in_url

        self.browser.setUrl(QUrl(url))

    def updateUrl(self, url):
        self.url_bar.setText(url.toString())
 

app = QApplication(sys.argv)
QApplication.setApplicationName("The Browser By Samin")
QApplication.setWindowIcon(QtGui.QIcon("Images\\home.png"))
window = mainWindow()
app.exec_()
