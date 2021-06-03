# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerJQqzFH.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.url_bar = QLineEdit(self.centralwidget)
        self.url_bar.setObjectName(u"url_bar")
        self.url_bar.setGeometry(QRect(190, 20, 241, 20))
        self.url_bar.setStyleSheet(u"\n"
"border: 1px solid gray;/*Set the thickness and color of the border*/\n"
" border-radius: 10px;/*Set the size of the rounded corners*/\n"
" padding: 0 8px;/*If there is no content, the cursor moves back by 0.8 pixels*/\n"
"selection-background-color: darkgray;\n"
"")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

