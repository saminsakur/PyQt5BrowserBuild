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
        self.setStyleSheet(
            """
            QLineEdit{
                font-family: \"Segoe UI\";
                padding-top:4px;
                padding-left:8px;
                padding-bottom:4px;
                border:2px solid transparent;
                border-radius:6px;
                font-size:10pt;
                background-color: #ffffff;
                selection-background-color: #66c2ff;
            }

            QLineEdit:focus{
                border-color:#3696ff;
            }

            QLineEdit:hover{
                border-color:#d6d6d6
            }
            
        """
        )


class SSLIcon(QLabel):
    def __init__(self):
        super().__init__()
        self.InitSSLIcon()

    def InitSSLIcon(self):
        self.setObjectName("SSLIcon")
        self.setPixmap(QPixmap(os.path.join("resources", "lock-icon.png")))


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
        self.setStyleSheet(
            """
            QTabBar{
                background-color:#2E385C;
            }

            QTabBar::tab {
                background-color: none;
                color: #fff;
                padding: 6px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding-right:60px;
                max-width:80px;
            }

            QTabBar::tab:!selected{
                background-color: transparent;
            }

            QTabBar::close-button {                         /* style the tab close button */
                image: url(./resources/closetabbutton.png);
                subcontrol-position: right;
                border: 1px solid transparent;
                border-radius:3px;
            }

            QTabBar::close-button:hover{                    /* close button hover */
                background-color: #3B2E53;
            }

            QTabWidget::tab-bar {
                left: 5px;                                  /* move to the right by 5px */
            }

            QTabBar::tab:!selected:hover{
                background-color:#222348;
            }

            QTabBar::tab:selected{                          /* selected tabs */
                background-color: #170733;
            }
        """
        )


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
