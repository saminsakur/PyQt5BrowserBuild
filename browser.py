import os
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class mainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__(*args, **kwargs)
        
        self.browser = QWebEngineView()
        self.tabs = QTabWidget()
        self.showMaximized()

        self.setCentralWidget(self.tabs)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.add_new_tab(QUrl("https://www.google.com"), "Google")

    
    # doubleclick on empty space for new tab
    def tab_open_doubleclick(self, i):
        if i == -1: # No tab under the click
            self.add_new_tab(QUrl("http://www.google.com/"), label="New tab")

    
    def close_current_tab(self, i):
        self.tabs.removeTab(i)

    # function to add new tab
    def add_new_tab(self, qurl=None, label="Blank"):
        self.browser.setUrl(qurl)
        # i = self.tabs.addTab(self.browser, label)
        # self.tabs.setCurrentIndex(i)
        self.tabs.addTab(self.browser, "Label")

app = QApplication(sys.argv)
window = mainWindow()
app.exec_()