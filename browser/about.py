import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QDialog,
    QMessageBox,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QWidget,
)


class AboutDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.layout = QVBoxLayout()

        ok_btn = QDialogButtonBox.Ok
        self.button_box = QDialogButtonBox(ok_btn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet("""
        QPushButton {
            background-color: #2B5DD1;
            color: #FFFFFF;
            border-style: outset;
            padding: 2px;
            font: bold 20px;
            border-width: 6px;
            border-radius: 10px;
            border-color: #2752B8;
        }
        QPushButton:hover {
            background-color: lightgreen;
        }

        """)


        logo = QLabel()
        pixmap = QPixmap(os.path.join("Icons", "browser.png"))
        pixmap = pixmap.scaled(60, 60)
        logo.setPixmap(pixmap)
        self.layout.addWidget(logo)

        title = QLabel("Simple Web Browser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        self.layout.addWidget(title)

        self.layout.addWidget(QLabel("Version 2.3"))

        lbl1 = QLabel("Copyright ©2021 <a href=\"https://github.com/saminsakur\">Samin Sakur</a>.")
        lbl1.setOpenExternalLinks(True)
        self.layout.addWidget(lbl1)
        
        github_pg = QLabel("<a href=\"https://github.com/saminsakur/PyQt5BrowserBuild\">Learn More </a>")
        github_pg.setOpenExternalLinks(True)
        self.layout.addWidget(github_pg)

        for i in range(0, self.layout.count()):
            self.layout.itemAt(i).setAlignment(Qt.AlignHCenter)
        
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)
