import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import QWebEngineView



class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # nav bar
        navbar = QToolBar()
        self.addToolBar(navbar)
        
        # back button
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

        # Home button
        home_button = QAction('Home', self)
        home_button.triggered.connect(self.goToHome)
        navbar.addAction(home_button)
        

    def goToHome(self):
        self.browser.setUrl(QUrl('https://www.google.com/'))




app = QApplication(sys.argv)
QApplication.setApplicationName("The Browser By Samin")
window = mainWindow()
app.exec_()
