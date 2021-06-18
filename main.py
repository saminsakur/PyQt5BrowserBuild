import os
import pyperclip as pc
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *



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
    "apple",
    "localhost"
)


class fileErrorDialog(QMessageBox):
    def __init__(self, *args, **kwargs):
        super(fileErrorDialog, self).__init__(*args, **kwargs)

        self.setText("Wrong file entered, Enter a correct file and try again.")
        self.setIcon(QMessageBox.Critical)

        self.setWindowTitle("Please enter a correct file")
        self.show()



class errorMsg(QMessageBox):
    def __init__(self):
        super(errorMsg, self).__init__()

        self.setText("An internal error occured!")
        self.setIcon(QMessageBox.Critical)

        self.setWindowTitle("Error!")
        self.show()




class PrintHandler(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.m_page = None
        self.m_inPrintPreview = False

    def setPage(self, page):
        assert not self.m_page
        self.m_page = page
        self.m_page.printRequested.connect(self.printPreview)

    @pyqtSlot()
    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self.m_page.view())
        if dialog.exec_() != QDialog.Accepted:
            return
        self.printDocument(printer)

    @pyqtSlot()
    def printPreview(self):
        if not self.m_page:
            return
        if self.m_inPrintPreview:
            return
        self.m_inPrintPreview = True
        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self.m_page.view())
        preview.paintRequested.connect(self.printDocument)
        preview.exec()
        self.m_inPrintPreview = False

    @pyqtSlot(QPrinter)
    def printDocument(self, printer):
        loop = QEventLoop()
        result = False

        def printPreview(success):
            nonlocal result
            result = success
            loop.quit()

        # progressbar to show loading
        progressbar = QProgressDialog(self.m_page.view())
        progressbar.findChild(QProgressBar).setTextVisible(False)
        progressbar.setLabelText("Please wait...")
        progressbar.setRange(0, 0)
        progressbar.show()
        progressbar.canceled.connect(loop.quit)
        self.m_page.print(printer, printPreview)
        loop.exec_()
        progressbar.close()

        if not result:
            painter = QPainter()
            if painter.begin(printer):
                font = painter.font()
                font.setPixelSize(20)
                painter.setFont(font)
                painter.drawText(QPointF(10, 25), "We could not generate print preview.")
                painter.end()




class mainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__()

        # create tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Add some styles to the tabs
        self.tabs.setStyleSheet("""
            
             QTabBar{
                background-color:#417294;
            }

            QTabBar::tab {
                background-color: none;
                color: #fff;
                padding: 6px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding-right:60px;
            }

            QTabBar::tab:!selected{
                background-color: transparent;
            }
            

            QTabBar::tab:selected, QTabBar::tab:hover {     /* not selected tabs */
                background-color: #4e88b1;
            }

            QTabBar::close-button {    /* style the tab close button */
                image: url(./Images/closetabbutton.png);
                subcontrol-position: right;
                border: 1px solid transparent;
                border-radius:3px;
            }

            QTabBar::close-button:hover{    /* close button hover */
                background-color: #3f84a6;
            }

            QTabWidget::tab-bar {
                left: 5px; /* move to the right by 5px */
            }

            QTabBar::tab:selected{  /* selected tabs */
                background-color: #005a87;
            }
        """)

        # Add new tab when tab tab is doubleclicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # To connect to a function when currrent tab has been changed
        self.tabs.currentChanged.connect(self.tab_changed)

        # Set the tabs closable
        self.tabs.setTabsClosable(True)

        # Function to handle tab closing
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # open new tab when Ctrl+T pressed
        AddNewTabKeyShortcut = QShortcut("Ctrl+T", self)
        AddNewTabKeyShortcut.activated.connect(lambda: self.add_new_tab(QtCore.QUrl("https://www.google.com/"), "New tab"))

        # Close current tab on Ctrl+W
        CloseCurrentTabKeyShortcut = QShortcut("Ctrl+W", self)
        CloseCurrentTabKeyShortcut.activated.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))

        # Exit browser on shortcut Ctrl+Shift+W
        ExitBrowserShortcutKey = QShortcut("Ctrl+Shift+W", self)
        ExitBrowserShortcutKey.activated.connect(sys.exit)


        # nav bar
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.addToolBar(self.navbar)

        # back button
        back_btn = QPushButton(self)
        back_btn.setObjectName("back_btn")
        back_btn.setIcon(QtGui.QIcon(os.path.join("Images", "left-arrow.png")))
        back_btn.setToolTip("Back to previous page")
        back_btn.setShortcut("Alt+Left")
        back_btn.clicked.connect(self.navigate_back_tab)
        self.navbar.addWidget(back_btn)

        # forward button
        forward_butn = QPushButton(self)       
        forward_butn.setObjectName("forward_butn")
        forward_butn.setIcon(QtGui.QIcon(os.path.join("Images", "right-arrow.png")))
        forward_butn.setToolTip("Go forward")
        forward_butn.setShortcut("Alt+Right")
        forward_butn.clicked.connect(self.forward_tab)
        self.navbar.addWidget(forward_butn)

        # Refresh button
        self.reload_butn = QPushButton(self)
        self.reload_butn.setObjectName("reload_butn")
        self.reload_butn.setToolTip("Reload current page")
        self.reload_butn.setShortcut("Ctrl+R")
        self.reload_butn.resize(QSize(50, 50))
        self.reload_butn.setIcon(QtGui.QIcon(os.path.join("Images", "refresh.png")))
        self.reload_butn.clicked.connect(self.reload_tab)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setObjectName("stop_butn")
        self.stop_btn.setToolTip("Stop loading current page")
        self.stop_btn.setShortcut("Escape")
        self.stop_btn.setIcon(QIcon(os.path.join('Images', 'cross.png')))
        self.stop_btn.clicked.connect(self.stop_loading_tab)

        # Added stop button 
        self.stop_action = self.navbar.addWidget(self.stop_btn)

        # Added reload button
        self.reload_action = self.navbar.addWidget(self.reload_butn)

        # Home button
        self.home_button = QPushButton(self)
        self.home_button.setObjectName("home_button")
        self.home_button.setToolTip("Back to home")
        self.home_button.setIcon(QtGui.QIcon(os.path.join("Images", "home.png")))
        self.home_button.clicked.connect(self.goToHome)
        self.navbar.addWidget(self.home_button)

        
        # Add Address bar
        self.url_bar = QLineEdit()
        self.url_bar.setFrame(False)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setShortcutEnabled(True)
        self.url_bar.setToolTip(self.url_bar.text())

        # Set focus on the Addressbar by pressing Ctrl+E
        FocusOnAddressBar = QShortcut("Ctrl+E", self)
        FocusOnAddressBar.activated.connect(self.url_bar.setFocus)


        # Set the placeholder text
        self.url_bar.setPlaceholderText("Search or enter web address")

        self.url_bar.setFocus()
        self.url_bar.setStyleSheet("""
            QLineEdit{
                font-family: Segoe UI;
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
            
        """)

        # Set stop action to be invisible
        self.stop_action.setVisible(False)

        # Add a separator
        self.navbar.addSeparator()

        # Shows ssl security icon
        self.httpsicon = QLabel()
        self.httpsicon.setObjectName("SSLIcon")
        self.httpsicon.setPixmap(QPixmap(os.path.join('Images', 'lock-icon.png')))

        # Add http icon to the navbar bar
        self.navbar.addWidget(self.httpsicon)

        # Add Address Bar to the navbar
        self.navbar.addWidget(self.url_bar)

        # The conetext menu
        context_menu = QMenu(self)


        # Set the object's name
        context_menu.setObjectName("ContextMenu")
        
        # Button for the three dot context menu button
        ContextMenuButton = QPushButton(self)
        ContextMenuButton.setObjectName("ContextMenuButton")

        # Enable three dot menu by pressing Alt+F
        ContextMenuButton.setShortcut("Alt+F")

        # Give the three dot image to the Qpush button
        ContextMenuButton.setIcon(QIcon(os.path.join("Images", "more.png")))    # Add icon
        ContextMenuButton.setObjectName("ContextMenuTriggerButn")
        ContextMenuButton.setToolTip("More")

        # Add the context menu to the three dot context menu button
        ContextMenuButton.setMenu(context_menu)


        """Actions of the three dot context menu"""

        # Add new tab
        newTabAction = QAction("New tab", self)
        newTabAction.setIcon(QtGui.QIcon(os.path.join("Images", "newtab.png")))
        newTabAction.triggered.connect(lambda: self.add_new_tab(QUrl("https://www.google.com/"), "Homepage"))
        newTabAction.setToolTip("Add a new tab")
        context_menu.addAction(newTabAction)

        # Close tab action
        CloseTabAction = QAction("Close tab", self)
        CloseTabAction.setIcon(QIcon(os.path.join("Images", "closetab.png")))
        CloseTabAction.triggered.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))
        CloseTabAction.setToolTip("Close current tab")
        context_menu.addAction(CloseTabAction)

        # A separator
        context_menu.addSeparator()

        # Feature to navigate to bing
        GoToBingAction = QAction("Bing", self)
        GoToBingAction.setIcon(QIcon(os.path.join("Images", "globe.png")))
        GoToBingAction.triggered.connect(self.GoToBing)
        GoToBingAction.setToolTip("https://www.bing.com/")
        context_menu.addAction(GoToBingAction)

        # Feature to navigate to DuckDuckGo
        GoToDuckDuckGo = QAction(QIcon(os.path.join("Images", "globe.png")), "DuckDuckgo", self)
        GoToDuckDuckGo.triggered.connect(self.NavigateDuckDuckGo)
        GoToDuckDuckGo.setToolTip("https://www.duckduckgo.com/")
        context_menu.addAction(GoToDuckDuckGo)

        # Another separator
        context_menu.addSeparator()

        # Feature to copy site url
        CopySiteAddress = QAction(QtGui.QIcon(os.path.join("Images", "url.png")), "Copy site url", self)
        CopySiteAddress.triggered.connect(self.CopySiteLink)
        CopySiteAddress.setToolTip("Copy current site address")
        context_menu.addAction(CopySiteAddress)

        # Fetaure to go to copied site url
        PasteAndGo = QAction(QtGui.QIcon(os.path.join("Images", "paste.png")), "Paste and go", self)
        PasteAndGo.triggered.connect(self.PasteUrlAndGo)
        PasteAndGo.setToolTip("Go to the an url copied to your clipboard")
        context_menu.addAction(PasteAndGo)

        # A separator
        context_menu.addSeparator()

        # Open page
        OpenPgAction = QAction("Open", self)
        OpenPgAction.setIcon(QtGui.QIcon(os.path.join("Images", "openclickhtml.png")))
        OpenPgAction.setToolTip("Open a file in this browser")
        OpenPgAction.setShortcut("Ctrl+O")
        OpenPgAction.triggered.connect(self.open_local_file)
        context_menu.addAction(OpenPgAction)

        # Save page as
        SavePageAs = QAction("Save page as", self)
        SavePageAs.setIcon(QtGui.QIcon(os.path.join("Images", "save-disk.png")))
        SavePageAs.setToolTip("Save current page to this device")
        SavePageAs.setShortcut("Ctrl+S")
        SavePageAs.triggered.connect(self.save_page)
        context_menu.addAction(SavePageAs)


        # Print this page action
        PrintThisPageAction = QAction("Print this page", self)
        PrintThisPageAction.setIcon(QtGui.QIcon(os.path.join("Images", "printer.png")))
        PrintThisPageAction.triggered.connect(self.print_this_page)
        PrintThisPageAction.setShortcut("Ctrl+P")
        PrintThisPageAction.setToolTip("Print current page")
        context_menu.addAction(PrintThisPageAction)

        # Print with preview
        PrintPageWithPreview = QAction(QtGui.QIcon(os.path.join("Images", "printerprev.png")), "Print with preview", self)
        PrintPageWithPreview.triggered.connect(self.PrintWithPreview)
        PrintPageWithPreview.setShortcut("Ctrl+Shift+P")
        context_menu.addAction(PrintPageWithPreview)

        # Save page as PDF
        SavePageAsPDF = QAction(QtGui.QIcon(os.path.join("Images", "adobepdf.png")), "Save as PDF", self)
        SavePageAsPDF.triggered.connect(self.save_as_pdf)
        context_menu.addAction(SavePageAsPDF)

        # The help submenu
        HelpMenu = QMenu("Help", self)
        HelpMenu.setObjectName("HelpMenu")
        HelpMenu.setStyleSheet(
        """
        background-color: #fff;
        background-color: #fdfdfd;
        border: 1px solid transparent;        
        font-family: Times, sans-serif;
        border-radius: 6px;

        QMenu#HelpMenu::item{
            background-color: transparent;
            font-size: 10pt;
            padding-left: 40px;
            padding-right: 100px;
            padding-top:10px;
            padding-bottom: 10px;
            width: 130px;
        }

        QMenu#HelpMenu::item:selected{
            background-color: #f2f2f2;
        }

        QMenu#HelpMenu::icon{
            padding-left:40px;
        }

        """)

        HelpMenu.setIcon(QIcon(os.path.join("Images", "question.png")))

        # About action
        AboutAction = QAction("About this browser", self)
        AboutAction.setIcon(QIcon(os.path.join("Images", "info.png")))
        AboutAction.triggered.connect(self.about)
        HelpMenu.addAction(AboutAction)

        # Visit action
        VisitGithubAction = QAction("Visit Github", self)
        VisitGithubAction.triggered.connect(self.visitGithub)
        HelpMenu.addAction(VisitGithubAction)

        context_menu.addMenu(HelpMenu)

        # Add a separator
        context_menu.addSeparator()


        # Close browser
        CloseBrowser = QAction("Close browser", self)
        CloseBrowser.triggered.connect(lambda: sys.exit())
        context_menu.addAction(CloseBrowser)

        """ 
        Set menu for the button
        ContextMenuButton.add
        Add the context menu to the navbar
        """

        self.navbar.addWidget(ContextMenuButton)
        
        # Stuffs to see at starup
        self.add_new_tab(QUrl("https://www.google.com/"), "Homepage")

        # Set the addressbar focus
        self.navbar.setFocus()

        # what to display on the window
        self.setCentralWidget(self.tabs)

        # Stuffs to set the window
        self.showMaximized()

        # Set minimum size
        self.setMinimumWidth(400)
    


    """Instead of managing 2 slots associated with the progress and completion of loading,
        only one of them should be used since, for example, the associated slot is also 
        called when it is loaded at 100% so it could be hidden since it can be invoked together with finished."""

    @QtCore.pyqtSlot(int)
    def loadProgressHandler(self, prog):
        if self.tabs.currentWidget() is not self.sender():
            return

        loading = prog < 100

        self.stop_action.setVisible(loading)
        self.reload_action.setVisible(not loading)



    # funcion to navigate to home when home icon is pressed   
    def goToHome(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com/"))


    # Function to navigate to bing by pressing go to bing on the three dot menu
    def GoToBing(self):
        self.add_new_tab(QUrl("https://www.bing.com/"), "Bing")


    # Function to navigate DuckDuckGo
    def NavigateDuckDuckGo(self):
        self.add_new_tab(QtCore.QUrl("https://www.duckduckgo.com/"), "DuckDuckGo")



    # Copy url of currently viewed page to clipboard
    def CopySiteLink(self):
        pc.copy(self.tabs.currentWidget().url().toString())


    # Adds a new tab and load the content of the clipboard
    def PasteUrlAndGo(self):
        self.add_new_tab(QUrl(pc.paste()), self.tabs.currentWidget().title())
    


    # Remove this if you don't need it
    def visitGithub(self):
        self.add_new_tab(QUrl("https://github.com/saminsakur/PyQt5BrowserBuild"), "Github")


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
        if self.tabs.currentWidget() is None:
            return

        self.tabs.currentWidget().stop()    


    """
    Functions to open a local file and save a website to user's local storage
    """
    # Function to open a local file
    def open_local_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open file", 
            directory="",
            filter="Hypertext Markup Language (*.htm *.html *.mhtml);;All files (*.*)"
            )
        if len(filename) > 0:
            try:
                with open(filename, "r", encoding="utf8") as f:
                    opened_file = f.read()
                    self.tabs.currentWidget().setHtml(opened_file)
                    
            except:
                dlg = fileErrorDialog()
                dlg.exec_()

        self.url_bar.setText(filename)



    # Function to save current site to user's local storage 
    def save_page(self):
        filepath, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save Page As", 
            directory="", 
            filter="Webpage, complete (*.htm *.html);;Hypertext Markup Language (*.htm *.html);;All files (*.*)",
        )
        try:
            if filter == "Hypertext Markup Language (*.htm *.html)":
                self.tabs.currentWidget().page().save(filepath, format=QWebEngineDownloadItem.MimeHtmlSaveFormat)
                
            elif filter == "Webpage, complete (*.htm *.html)":
                self.tabs.currentWidget().page().save(filepath, format=QWebEngineDownloadItem.CompleteHtmlSaveFormat)

        except:
             self.showErrorDlg()

    # Print handler
    def print_this_page(self):
        try:
            handler_print = PrintHandler()
            handler_print.setPage(self.tabs.currentWidget().page())
            handler_print.print()
        
        except:
            self.showErrorDlg()

    

    # Print page with preview
    def PrintWithPreview(self):
        handler = PrintHandler()
        handler.setPage(self.tabs.currentWidget().page())
        handler.printPreview()

    # Save as pdf
    def save_as_pdf(self):
        filename, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save as",
            filter="PDF File (*.pdf);;All files (*.*)"
        )
         
        self.tabs.currentWidget().page().printToPdf(filename)



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
    

    # Update window title
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()

        if 0 > len(title):
            self.setWindowTitle("{} - Simple Web Browser".format(title))

        else:
            self.setWindowTitle("Simple Web Browser")


    # To close current tab
    def close_tab(self, i):
        self.tabs.removeTab(i)
    

    # function to add new tab
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('https://www.google.com/')
        
        browser = QWebEngineView()  # Define the main webview to browser the internet

        # Full screen enble
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        browser.page().fullScreenRequested.connect(lambda request: request.accept())

        browser.loadProgress.connect(self.loadProgressHandler)

        browser.page().WebAction(QWebEnginePage.OpenLinkInNewTab)

        browser.settings().setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        # browser.setPage(customQWebEnginePage)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.load(qurl)
        self.url_bar.setFocus()


        # update url when it's from the correct tab
        # update url when it's from the correct tab
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))


    def showErrorDlg(self):
        dlg = errorMsg()
        dlg.exec_()


    def about(self):
        dialouge = AboutDialog()
        dialouge.exec_()


    # Update address bar to show current pages's url
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            # if signal is not from the current tab, then ignore
            return
        
        if q.scheme() == 'https':
            # secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "security.png")))
            self.httpsicon.setToolTip("Connection to this is is secure\n\nThis site have a valid certificate")
        
        elif q.scheme() == "file":
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "file-protocol.png")))
            self.httpsicon.setToolTip("You are viewing a local or shared file")
        
        elif q.scheme() == "data":
            self.httpsicon.setPixmap(QPixmap(os.path.join("Images", "file-protocol.png")))
            self.httpsicon.setToolTip("You are viewing a local or shared file")

        
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
        """ if the text in the search box endswith one of the domain in the domains tuple, then "http://" will be added
         if the text is pre "http://" or "https://" added, then not"""               
        # [0-9A-Za-z]+\.+[A-Za-z0-9]{2}

        if self.tabs.currentWidget is None: # To avoid exception
            # If QTabWidget's currentwidet is none, the ignore
            return

        if QUrl(in_url).scheme() == "file":
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.tabs.currentWidget().load(local_url)
            

        elif any([in_url.endswith(domains), in_url.endswith("/")]) and not any(i in in_url  for i in ("http://","https://","file:///")):
            url = "http://"+in_url

        # this will search google
        elif not any(i in in_url for i in domains) or not any(i in in_url  for i in("http:", "https:", "/")):
            url = self.searchGoogle(in_url)
                
        # else browser will go to anything the user has been written
        else:
            url = in_url
        
        self.tabs.currentWidget().load(QUrl.fromUserInput(url))




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




def main():
    app = QApplication(sys.argv)

    # Set the window name
    QApplication.setApplicationName("Simple Web Browser")

    # Set the window icon
    QApplication.setWindowIcon(QIcon(os.path.join("Icons", "browser.png")))

    # App styles
    app.setStyleSheet("""
    QPushButton#ContextMenuTriggerButn::menu-indicator{ /* Hide context menu button dropdown icon */
        image: none;
    }

    QToolBar {
        background-color: #edf4f7;
    }
    

    /* Style all contextmenus*/

    Qmenu{
        background-color:fff;
    }


    /* Style right arrow of QMenu */

    QMenu::right-arrow{
        image :url(Images/right-arrow-context-menu.png);
        height:12px;
        width:12px;
    }

    QMenu::item{    /* Styling all contextmenus */
        background-color: transparent;
        font-size: 10pt;
        padding-left: 10px;
        padding-right: 100px;
        padding-top:5px;
        padding-bottom: 5px;
        width: 120px;
    }

    QMenu::item:selected{
        background-color: #dedeff;
    }

    /*
     The three dot menu 
    */

    QMenu#ContextMenu {
        background-color: #fdfdfd;
        border: 1px solid transparent;        
        font-family: Times, sans-serif;
        border-radius: 6px;
    }

    QMenu#ContextMenu::item {
        background-color: transparent;
        font-size: 10pt;
        padding-left: 40px;
        /*padding-right: 100px;*/
        padding-top:8px;
        padding-bottom: 8px;
        width: 130px;
    }

    QMenu#ContextMenu::icon{
        padding-left:40px;
    }

    QMenu#ContextMenu::separator {
        height: 1px;
        background: #111;
        margin-left: 0%;
        margin-right: 0%;
    }

    QMenu#ContextMenu::item:selected{
        background-color: #f2f2f2;
    }

    /*
     Styling of toolip
    */

    QToolTip{
        background-color:#131c21;
        font-size: 10pt;
        opacity:200;
        color: #f1f1f1;
        border-radius:10px;
        padding:5px;
        border-width:2px;
        border-style:solid;
        border-radius:20px;
        border: 2px solid transparent;
    }
    

    /* SSLinfo label */

    QLabel#SSLIcon {    /* ssl icon */
        border: 1px solid transparent;
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 6px;
        width: 5px;
        height: 5px;
    }


    /* Button styling */

    QPushButton#ContextMenuTriggerButn {    /* Context menu button */
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 16px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#back_btn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#forward_butn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#reload_butn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#home_button {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }

    QPushButton#stop_butn {
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 7px;
        width: 10px;
        height: 10px;
        background-color: none;
    }


    /*
    * after hover
    */

    QPushButton#stop_butn:hover {
        background-color: #dce9ef;
    }

    QPushButton#back_btn:hover {
        background-color: #dce9ef;
    }

    QPushButton#forward_butn:hover {
        background-color: #dce9ef;
    }

    QPushButton#reload_butn:hover {
        background-color: #dce9ef;
    }

    QPushButton#home_button:hover {
        background-color: #dce9ef;
    }

    QPushButton#ContextMenuTriggerButn:hover {
        background-color: #dce9ef;
    }

    /*
    * after pressed
    */

    QPushButton#stop_butn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#back_btn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#forward_butn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#reload_butn:pressed {
        background-color: #cadfe7;
    }

    QPushButton#home_button:pressed {
        background-color: #cadfe7;
    }

    QPushButton#ContextMenuTriggerButn:pressed {
        background-color: #cadfe7;
    }

    """)



    #e6e6e6 background color
    window = mainWindow()
    window.show()
    try:
        sys.exit(app.exec_())

    except SystemExit:
        print("Closing browser...")


if __name__ == "__main__":
    main()







