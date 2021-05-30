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


app = QApplication(sys.argv)
QApplication.setApplicationName("The Browser By Samin")
window = mainWindow()
app.exec_()
