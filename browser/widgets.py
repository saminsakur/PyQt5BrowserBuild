import os

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QLabel, QLineEdit, QTabWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import QtCore


class AddressBar(QLineEdit):
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
        with open(os.path.join("styles", "addr_bar.css")) as f:
            self.setStyleSheet(f.read())


class SSLIcon(QLabel):
    def __init__(self):
        super().__init__()
        self.InitSSLIcon()

    def InitSSLIcon(self):
        self.setObjectName("SSLIcon")
        icon = QPixmap(os.path.join("resources", "lock-icon.png"))
        self.setPixmap(icon)


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setDocumentMode(True)

        # Set the tabs closable
        self.setTabsClosable(True)

        # Set the tabs movable
        self.setMovable(True)

        # Add font family
        font = QFont("Segoe UI", 8)
        self.setFont(font)

        # Add some styles to the tabs
        with open(
            os.path.join("styles", "tab_style.css")
        ) as f:  # Open tab_styles.css file
            self.setStyleSheet(f.read())


class customWebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = customWebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @QtCore.pyqtSlot(QtCore.QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()
