import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QWidget


class AboutDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        ok_btn = QDialogButtonBox.Ok
        self.button_box = QDialogButtonBox(ok_btn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('Icons', 'browser.png')))
        
        self.layout.addWidget(logo)
        