import json
import os
from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtWidgets import QWidget

from . import settings_data

class UserSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.default_search_engine = settings_data["defaultSearchEngine"]
        self.mainWidget = QWidget(self)

        self.init_ui()
        self.retranslateUi()

    def init_ui(self):
        self.resize(706, 485)
        self.addDefaultSearchEngineSelector()

        # Add settings title
        self.label_2 = QtWidgets.QLabel(self.mainWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet('font: 12pt "Segoe UI";')
        self.label_2.setObjectName("label_2")

        # Close button
        self.closeButn = QtWidgets.QPushButton(self.mainWidget)
        self.closeButn.setGeometry(QtCore.QRect(660, 10, 33, 33))
        self.closeButn.setIcon(QtGui.QIcon(os.path.join("resources", "cross.png")))
        self.closeButn.setObjectName("closeButn")
        self.closeButn.clicked.connect(self.closeWindow)

        self.startup_page = QtWidgets.QLineEdit(self.mainWidget)
        self.startup_page.setGeometry(QtCore.QRect(480, 150, 211, 33))
        self.startup_page.setText(settings_data["startupPage"])
        self.startup_page.setObjectName("startup_page")

        # On startup section
        self.label_3 = QtWidgets.QLabel(self.mainWidget)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label = QtWidgets.QLabel(self.mainWidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Home button section
        self.label_7 = QtWidgets.QLabel(self.mainWidget)
        self.label_7.setGeometry(QtCore.QRect(10, 230, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        # Home button page
        self.home_button_page = QtWidgets.QLineEdit(self.mainWidget)
        self.home_button_page.setGeometry(QtCore.QRect(480, 250, 211, 33))
        self.home_button_page.setText(settings_data["homeButtonPage"])
        self.home_button_page.setObjectName("home_button_page")

        # New tab open settings
        self.label_9 = QtWidgets.QLabel(self.mainWidget)
        self.label_9.setGeometry(QtCore.QRect(10, 330, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        # Page to open on each tab
        self.new_tab_page = QtWidgets.QLineEdit(self.mainWidget)
        self.new_tab_page.setText(settings_data["newTabPage"])
        self.new_tab_page.setGeometry(QtCore.QRect(480, 360, 211, 33))
        self.new_tab_page.setObjectName("new_tab_page")

        # these are all descriptions
        self.label_4 = QtWidgets.QLabel(self.mainWidget)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 235, 20))
        self.label_4.setObjectName("label_4")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_4.setFont(font)

        self.label_5 = QtWidgets.QLabel(self.mainWidget)
        self.label_5.setGeometry(QtCore.QRect(10, 90, 270, 20))
        self.label_5.setObjectName("label_5")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_5.setFont(font)

        self.label_6 = QtWidgets.QLabel(self.mainWidget)
        self.label_6.setGeometry(QtCore.QRect(10, 260, 360, 20))
        self.label_6.setObjectName("label_6")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_6.setFont(font)

        self.label_8 = QtWidgets.QLabel(self.mainWidget)
        self.label_8.setGeometry(QtCore.QRect(10, 360, 320, 20))
        self.label_8.setObjectName("label_8")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_8.setFont(font)

        # Save button
        self.save_settings = QtWidgets.QPushButton(self.mainWidget)
        self.save_settings.setGeometry(QtCore.QRect(572, 440, 121, 33))
        self.save_settings.setObjectName("save_settings")
        self.save_settings.clicked.connect(self.saveChangesToJson)

        # Discard button
        self.discard_changes = QtWidgets.QPushButton(self.mainWidget)
        self.discard_changes.setGeometry(QtCore.QRect(430, 440, 121, 33))
        self.discard_changes.setObjectName("discard_changes")
        self.discard_changes.clicked.connect(self.closeWindow)

        QtCore.QMetaObject.connectSlotsByName(self.mainWidget)
        self.setStyleSheet(
            """
            QWidget{
                background-color:#F7F7F7;
            }
            QPushButton#closeButn{
                border: 1px solid transparent;
                border-radius: 3px;
            }
            QPushButton#closeButn:hover{
                background-color:#d1d1d1;
            }
            QLineEdit{
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px 5px;
                height: 60px;
                font-size: 12px;
            }
            QComboBox{
                border: 2px solid #ccc;
                border-radius:5px;
                padding: 5px 5px;
            }
            QComboBox::down-arrow{
                image: url(./resources/arrow-down-12.png);
                border : none;
            }
            QComboBox::drop-down{
                border: none;
            }
            QPushButton#save_settings{
                font-size: 10pt;
                padding: 5px;
                border: 1px solid darkgray;
                border-radius: 7px;
                background-color: #2781F2;
                color: #ffffff;
            }
            QPushButton#discard_changes{
                font-size: 10pt;
                background: transparent;
                border: 1px solid #FF0000;
                border-radius: 7px;
                padding:5px;
            }
            QPushButton#save_settings:hover{
                background-color: #3185eb;
            }
            QPushButton#save_settings:pressed{
                background-color: #387cd1;
            }
            QPushButton#discard_changes:hover{
                background-color: #E81123;
                color: #fff;
            }
            QPushButton#discard_changes:pressed{
                background-color: #9B0B17;
            }
            QLabel#label_4, QLabel#label_5, QLabel#label_6, QLabel#label_8{
                color: #606770;
            }
            """
        )

    # Add drop-down menu to select default search engine
    def addDefaultSearchEngineSelector(self):
        self.searchEngineSelector = QtWidgets.QComboBox(self.mainWidget)
        self.searchEngineSelector.setEnabled(True)
        self.searchEngineSelector.setGeometry(QtCore.QRect(480, 80, 211, 33))

        # Search engines
        self.searchEngineSelector.addItem("Google")
        self.searchEngineSelector.addItem("Yahoo")
        self.searchEngineSelector.addItem("Bing")
        self.searchEngineSelector.addItem("DuckDuckGo")
        self.searchEngineSelector.currentTextChanged.connect(self.addDropDownItemToJson)

        if self.default_search_engine == "Google":
            self.searchEngineSelector.setCurrentIndex(0)
        elif self.default_search_engine == "Yahoo":
            self.searchEngineSelector.setCurrentIndex(1)
        elif self.default_search_engine == "Bing":
            self.searchEngineSelector.setCurrentIndex(2)
        elif self.default_search_engine == "DuckDuckGo":
            self.searchEngineSelector.setCurrentIndex(3)

    # Write to json

    def saveChangesToJson(self):  # startup pg
        if len(self.startup_page.text()) > 0:
            settings_data["startupPage"] = self.startup_page.text()
            with open("settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)

        if len(self.home_button_page.text()) > 0:
            settings_data["homeButtonPage"] = self.home_button_page.text()
            with open("settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)

        if len(self.new_tab_page.text()) > 0:
            settings_data["newTabPage"] = self.new_tab_page.text()
            with open("settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)

    def addDropDownItemToJson(self):
        settings_data["defaultSearchEngine"] = self.searchEngineSelector.currentText()
        with open("settings.json", "w") as f:
            json.dump(settings_data, f, indent=2)

    def closeWindow(self):
        self.close()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("Form", "Settings"))
        self.label_3.setText(_translate("Form", "On startup"))
        self.save_settings.setText(_translate("Form", "Save settings"))
        self.label.setText(_translate("Form", "Default Search Engine"))
        self.label_4.setText(
            _translate("Form", "Choose what page to display on startup")
        )
        self.label_5.setText(
            _translate("Form", "Default search engine used in the address bar")
        )
        self.label_6.setText(
            _translate(
                "Form", "Choose what page to navigate when home button is pressed"
            )
        )
        self.label_7.setText(_translate("Form", "Home button"))
        self.label_8.setText(
            _translate("Form", "Choose what page to show when a new tab is opened")
        )
        self.label_9.setText(_translate("Form", "New tab"))
        self.discard_changes.setText(_translate("Form", "Discard changes"))

