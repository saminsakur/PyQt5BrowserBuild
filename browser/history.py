from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QListWidget, QPushButton, QWidget, QLabel
import browser
import browser.main_window

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()

        titleLbl = QLabel("History")
        titleLbl.setStyleSheet(
            """
            margin-top:7px;
        """
        )
        titleLbl.setFont(browser.textFont)

        clearBtn = QPushButton("Clear")
        clearBtn.setObjectName("ClearButnHistory")
        clearBtn.setFont(browser.textFont)
        clearBtn.setStyleSheet(
            """
            QPushButton#ClearButnHistory{
                border:1px solid transparent;
                border-radius: 7px;
                border-color:#ccc;
                margin-top:6px;
                margin-left:80px;
                margin-right:10px;
                padding: 5px 5px 5px 5px;
                font-size:12pt;
                color:#000;
                background-color:transparent;
            }

            QPushButton#ClearButnHistory:hover{
                background-color:#2681f2;
                border-color:#dae0e5;
                color: #fff;
            }

            QPushButton#ClearButnHistory:pressed{
                background-color:#0c63ce;
            }          
            """
        )
        clearBtn.clicked.connect(self.clearHistory)

        self.historyList = QListWidget()
        # self.historyList.horizontalScrollBar().setEnabled(False)
        self.historyList.horizontalScrollBar().setStyleSheet(
            """
                QScrollBar:horizontal {
                    height:8px;
                }
                QScrollBar::handle:horizontal {
                    background: gray;
                    min-height: 5px;
                    border: 1px solid gray;
                    border-radius: 4px;
                }
                QScrollBar::left-arrow:horizontal {
                    background:none;
                }
                QScrollBar::right-arrow:horizontal {
                    background:none;
                }
            """
        )
        self.historyList.verticalScrollBar().setStyleSheet(
            """
            QScrollBar:vertical {
                background: transparent;
                width:8px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: gray;
                min-width: 5px;
                border: 1px solid gray;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical{
                background:none;
            }
            QScrollBar::sub-line:vertical{
                background:none;
            }
        """
        )

        self.fillHistoryList()

        self.historyList.itemClicked.connect(self.goClickedLink)
        self.historyList.setStyleSheet(
            """
        QListWidget::item{
            padding-top: 8px;
            padding-bottom: 8px;
            margin-top: 2px;
            margin-bottom: 2px;
        }

        QListWidget::item:hover{
            background-color:#dce9ef;
        }
        
        QListWidget{
            border: 1px solid transparent;
            border-top: 1px solid gray;
            padding-left:5px;
            padding-right:5px;
        }
        """
        )

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

