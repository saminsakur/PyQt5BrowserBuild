from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QListWidget, QPushButton, QWidget, QLabel
import browser
import browser.main_window
import os


class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()

        titleLbl = QLabel("History")
        titleLbl.setFont(browser.textFont)

        clearBtn = QPushButton("Clear")
        clearBtn.setObjectName("ClearButnHistory")
        clearBtn.setFont(browser.textFont)
        clearBtn.clicked.connect(self.clearHistory)

        self.historyList = QListWidget()
        # self.historyList.horizontalScrollBar().setEnabled(False)

        self.fillHistoryList()

        self.historyList.itemClicked.connect(self.goClickedLink)

        with open(os.path.join("styles", "history_style.css")) as f:
            style = f.read()
            clearBtn.setStyleSheet(style)
            self.historyList.setStyleSheet(style)
            self.historyList.horizontalScrollBar().setStyleSheet(style)
            self.historyList.verticalScrollBar().setStyleSheet(style)

        layout = QGridLayout()

        layout.addWidget(titleLbl, 0, 0)
        layout.addWidget(clearBtn, 0, 1)
        layout.addWidget(self.historyList, 1, 0, 1, 2)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def fillHistoryList(self):
        data = browser.cursor.execute("SELECT * FROM history")
        siteInfoList = data.fetchall()
        for i in range(len(siteInfoList) - 1, -1, -1):
            siteInfo = siteInfoList[i][1] + " - " + siteInfoList[i][3]
            self.historyList.addItem(siteInfo)

    def goClickedLink(self, item):
        siteName = item.text()
        visitDate = siteName[len(siteName) - 19 :]
        siteInfoFromDB = browser.cursor.execute(
            "SELECT * FROM history WHERE date = ?", [visitDate]
        )
        try:
            url = siteInfoFromDB.fetchall()[0][2]
            w = browser.main_window.mainWindow()
            w.openSiteHistoryClicked(
                QtCore.QUrl(url), str(siteName)
            )  # open selected url
        except:
            self.close()

        self.close()

    def clearHistory(self):
        self.historyList.clear()
        browser.cursor.execute("DELETE FROM history")
        browser.connection.commit()
