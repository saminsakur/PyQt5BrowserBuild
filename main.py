import os
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
        
        # define webview
        self.browser = QWebEngineView()
        # create tabs
        self.tabs = QTabWidget()
        self.tabs.setCurrentWidget(self.browser)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setStyleSheet("""
            QTabBar{
                background-color:#666664;
            }
            QTabBar::tab {
                background-color: #a3a3a3;
                color: #fff;
                padding: 6px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding-right:60px;
            }

            QTabBar::tab:focus{
                border-color:blue;
                background-color:#e3e3e3;
            }
            
            QTabBar::tab:hover{
                background-color:#848889;
            }
        """)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.browser.loadProgress.connect(self.loadProgressHandler)
        self.browser.loadFinished.connect(self.loadFinishedHandler)
        self.setCentralWidget(self.tabs)

        self.showMaximized()


        # nav bar
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.addToolBar(self.navbar)

        # back button
        back_btn = QPushButton(self)
        back_btn.setObjectName("back_btn")
        back_btn.setToolTip("Back to previous page")
        back_btn.setIcon(QtGui.QIcon(os.path.join("Images", "left-arrow.png")))
        back_btn.clicked.connect(self.navigate_back_tab)
        self.navbar.addWidget(back_btn)

        # forward button
        forward_butn = QPushButton(self)       
        forward_butn.setObjectName("forward_butn")
        forward_butn.setToolTip("Go forward")
        forward_butn.setIcon(QtGui.QIcon(os.path.join("Images", "right-arrow.png")))
        forward_butn.clicked.connect(self.forward_tab)
        self.navbar.addWidget(forward_butn)

        # Refresh button
        self.reload_butn = QPushButton(self)
        self.reload_butn.setObjectName("reload_butn")
        self.setToolTip("Reload current page")
        self.reload_butn.setIcon(QtGui.QIcon(os.path.join("Images", "refresh.png")))
        self.reload_butn.clicked.connect(self.reload_tab)

        # Set reload button visible
        self.reload_butn.setHidden(False)
        
        # Stop button
        self.stop_btn = QPushButton(self)
        self.stop_btn.setObjectName("stop_butn")
        self.stop_btn.setIcon(QIcon(os.path.join('Images', 'cross.png')))
        self.stop_btn.clicked.connect(self.stop_loading_tab)

        # Set stop_butn hidden initially
        self.stop_btn.setHidden(True)

        # Add Refresh and Stop button
        self.navbar.addWidget(self.stop_btn)
        self.navbar.addWidget(self.reload_butn)

        
        # Home button
        self.home_button = QPushButton(self)
        self.home_button.setObjectName("home_button")
        self.home_button.setToolTip("Back to home")
        self.home_button.setIcon(QtGui.QIcon(os.path.join("Images", "home.png")))
        # self.home_button.clicked.connect(self.goToHome)
        self.home_button.clicked.connect(self.goToHome)
        self.navbar.addWidget(self.home_button)
        

        
        # self.set_reload_icon(self.tabs.currentWidget())
        self.navbar.addSeparator()
        
        # Add Address bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            QLineEdit{
                font-family: Segoe UI;
                padding-top:4px;
                padding-left:8px;
                padding-bottom:4px;
                border:2px solid #dddddd;
                border-radius:6px;
                font-size:10pt;
                background-color:#fff;
            }

            QLineEdit:focus{
                border-color:#87CEEB
            }

            QLineEdit:hover{
                border-color:#e6e6e6
            }
        """)



        # Shows ssl security icon
        self.httpsicon = QLabel()
        self.httpsicon.setObjectName("SSLIcon")
        self.httpsicon.setPixmap(QPixmap(os.path.join('Images', 'lock-icon.png')))
        self.navbar.addWidget(self.httpsicon)
        
        # Add address bar to the nav bar
        self.navbar.addWidget(self.url_bar)

        # self.url_bar.mousePressEvent.connect(self.select_all_text)
        

        
        # tab_close_button = QPushButton("Close tab", self)
        # tab_close_button.setStyleSheet('''color:red;''')
        # tab_close_button.pressed.connect(self.close_current_tab)
        # self.tabs.addAction(tab_close_button)
        self.navbar.addSeparator()

        ContextMenuButton = QPushButton(self)
        ContextMenuButton.setObjectName("ContextMenuButton")
        ContextMenuButton.setIcon(QIcon(os.path.join("Images", "info.png")))
        ContextMenuButton.clicked.connect(self.about)
        ContextMenuButton.setObjectName("ContextMenuTriggerButn")
        self.navbar.addWidget(ContextMenuButton)

        test = QAction("Test", self)
        test.triggered.connect(self.blah)
        self.navbar.addAction(test)

        # on startup
        self.add_new_tab(QUrl("https://www.google.com/"), "Homepage")
        self.show()
    
    def blah(self):
            self.add_new_tab(QUrl("https://www.gmail.com"), "Samin Sakur")
    @QtCore.pyqtSlot(int)
    def loadProgressHandler(self, prog):
        self.stop_btn.setHidden(False)  # When any page is loading, then stop_butn will visible
        self.reload_butn.setHidden(True)    # When any page is loading, then reload_butn will hidde  

    @QtCore.pyqtSlot()
    def loadFinishedHandler(self):
        self.reload_butn.setHidden(False)    # When loading is finished, then reload_butn will be visible again for the user
        self.stop_btn.setHidden(True)   # When load finished, stop button will be hidden

    # funcion to navigate to home when home icon is pressed   
    def goToHome(self):
        self.browser.setUrl(QUrl("http://www.google.com/"))
    # navigate backward tab
    def navigate_back_tab(self):
        self.browser.back()

    # go forward tab
    def forward_tab(self):
        self.browser.forward()

    # reload tab
    def reload_tab(self):
        self.browser.reload()

    # stop load current tab
    def stop_loading_tab(self):
        self.browser.stop()

    # doubleclick on empty space for new tab
    def tab_open_doubleclick(self, i):
        if i == -1: # No tab under the click
            self.add_new_tab(QUrl("http://www.google.com/"), label="New tab")
    
    # to update the tab
    def tab_changed(self, i):
        qurl = self.browser.url()
        self.update_urlbar(qurl, self.browser)
        self.update_title(self.browser)

    # to close current tab
    def close_current_tab(self, i):
        if self.tabs.count() < 2 :
            return

        elif self.tabs.count() == 0:
            sys.exit()

        self.tabs.removeTab(i)
    
    def update_title(self, browser):
        if browser != self.browser:
            return

        title = self.browser.page().title()
        self.setWindowTitle("{} Simple Web Browser".format(title))

    # To close current tab
    def close_tab(self, i):
        self.tabs.removeTab(i)
    
    # function to add new tab
    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('')

        self.browser.setUrl(qurl)
        i = self.tabs.addTab(self.browser, label)

        self.tabs.setCurrentIndex(i)

        # More difficult! We only want to update the url when it's from the
        # correct tab
        self.browser.urlChanged.connect(lambda qurl, browser=self.browser:
                                   self.update_urlbar(qurl, browser))

        self.browser.loadFinished.connect(lambda _, i=i, browser=self.browser:
                                     self.tabs.setTabText(i, browser.page().title()))


    def select_all_text(self):
        self.url_bar.selectAll()

    def about(self):
        dialouge = AboutDialog()
        dialouge.exec_()

    def update_urlbar(self, q, browser=None):
        if browser != self.browser:    # if error, the change
            # if signal is not from the current tab, then ignore
            return
        
        if q.scheme() == 'https':
            # secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "security.png")))
            self.httpsicon.setToolTip("Connection to this is is secure\n\nThis site have a valid certificate")
        
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
        # if the text in the search box endswith one of the domain in the domains tuple, then "http://" will be added
        # if the text is pre "http://" or "https://" added, then not               
        # To open files
        # [0-9A-Za-z]+\.+[A-Za-z0-9]{2}
        
        if QUrl(in_url).scheme() == "file":
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.browser.load(local_url)
            

        elif any([in_url.endswith(domains), in_url.endswith("/")]) and not any(i in in_url  for i in ("http://","https://","file:///")):
            url = "http://"+in_url

        # this will search google
        elif not any(i in in_url for i in domains) or not any(i in in_url  for i in("http:", "https:", "/")):
            url = self.searchGoogle(in_url)
                
        # else browser will go to anything the user has been written
        else:
            url = in_url

        
        self.browser.setUrl(QUrl(url))

            



app = QApplication(sys.argv)
QApplication.setApplicationName("Simple Web Browser")
QApplication.setWindowIcon(QIcon(os.path.join("Images", "browser.png")))
app.setStyleSheet("""
QToolBar{
    background-color:#eee;
}

QLabel#SSLIcon{
    border:1px solid transparent;
    padding-left:10px;
    padding-right:10px;
    border-radius:6px;
    width:5px;
    height:5px;
}

QLabel#SSLIcon:hover{
    background-color:#e6e6e6;
}

QPushButton#ContextMenuTriggerButn{
    border:1px solid transparent;
    padding:10px;
    border-radius:16px;
    width:10px;
    height:10px;
    background-color:none;
}

QPushButton#back_btn{
    border:1px solid transparent;
    padding:10px;
    border-radius:7px;
    width:10px;
    height:10px;
    background-color:none;
}

QPushButton#forward_butn{
    border:1px solid transparent;
    padding:10px;
    border-radius:7px;
    width:10px;
    height:10px;
    background-color:none;   
}

QPushButton#reload_butn{
    border:1px solid transparent;
    padding:10px;
    border-radius:7px;
    width:10px;
    height:10px;
    background-color:none;    
}

QPushButton#home_button{
    border:1px solid transparent;
    padding:10px;
    border-radius:7px;
    width:10px;
    height:10px;
    background-color:none;    
}

QPushButton#stop_butn{
    border:1px solid transparent;
    padding:10px;
    border-radius:7px;
    width:30px;
    height:10px;
    background-color:none;    
}

/*
 * after hover
*/
QPushButton#stop_butn:hover{
    background-color:#e6e6e6;
}

QPushButton#back_btn:hover{
    background-color:#e6e6e6
}

QPushButton#forward_butn:hover{
    background-color:#e6e6e6
}

QPushButton#reload_butn:hover{
    background-color:#e6e6e6
}

QPushButton#home_button:hover{
    background-color:#e6e6e6
}

QPushButton#ContextMenuTriggerButn:hover{
    background-color:#ccc;
}          
""")
#e6e6e6 background color
window = mainWindow()
app.exec_()
