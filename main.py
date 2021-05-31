import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import QWebEngineView



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
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # forward button
        forward_butn = QAction('Forward', self)
        forward_butn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_butn)

        # Refresh button
        reload_butn = QAction('Reload', self)
        reload_butn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_butn)

        butn1 = QtWidgets.QPushButton(self)
        butn1.setText("click me")
        butn1.clicked.connect(self.goToHome)
        navbar.addWidget(butn1)


        # Home button
        home_button = QAction('Home', self)
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
        self.browser.setUrl(QUrl(self.url_bar.text()))    

    def updateUrl(self, url):
        self.url_bar.setText(url.toString())
 





app = QApplication(sys.argv)
QApplication.setApplicationName("The Browser By Samin")
window = mainWindow()
app.exec_()
