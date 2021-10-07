import os

from PyQt5.QtGui import QFont, QPixmap
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
        with open(os.path.join("browser", "styles", "about_style.css")) as f:
            self.button_box.button(QDialogButtonBox.Ok).setStyleSheet(f.read())

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

        lbl1 = QLabel(
            'Copyright ©2021 <a href="https://github.com/saminsakur">Samin Sakur</a>.'
        )
        lbl1.setOpenExternalLinks(True)
        self.layout.addWidget(lbl1)

        github_pg = QLabel(
            '<a href="https://github.com/saminsakur/PyQt5BrowserBuild">Learn More </a>'
        )

        font = QFont("Font Awesome 5 Free Solid6")
        github_pg.setFont(font)
        github_pg.setOpenExternalLinks(True)
        self.layout.addWidget(github_pg)

        for i in range(0, self.layout.count()):
            self.layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)
