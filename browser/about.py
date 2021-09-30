

class AboutDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        butn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(butn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.setStyleSheet(
            """
            QPushButton{
                border:1px solid transparent;
                border-radius: 7px;
                border-color:#ccc;
                padding-top: 8px;
                padding-bottom: 8px;
                padding-right: 30px;
                padding-left: 30px;
                font-size:12pt;
                color:#fff;
                background-color:#0E71EB;
            }

            QPushButton:hover{
                background-color:#2681F2;
                border-color:#dae0e5;
                color: #fff;
            }

            QPushButton:pressed{
                background-color:#0C63CE;
            }          
        """
        )

        layout = QVBoxLayout()

        image = QLabel()
        browserIcon = QPixmap(os.path.join("Icons", "browser.png"))
        browserIcon = browserIcon.scaled(60, 60)
        image.setPixmap(browserIcon)

        hint = QLabel("About")
        hint.setStyleSheet(
            """
        font-size: 18px;
        margin-bottom: 10px;
        """
        )

        title = QLabel("Simple Web Browser")
        title.setStyleSheet(
            """margin-left:100px;
               font-size: 24px;
            """
        )
        title.setFont(textFont)

        layout2 = QHBoxLayout()
        layout2.addWidget(image)
        layout2.addWidget(title)
        layout.addWidget(hint)
        layout.addLayout(layout2)

        text1 = QLabel("Learn more:\nhttps://github.com/saminsakur/PyQt5BrowserBuild")
        text1.setStyleSheet(
            """
            margin-top: 20px;
        """
        )

        text2 = QLabel("Made by Samin Sakur - https://github.com/saminsakur")
        text2.setStyleSheet(
            """
            margin-top: 20px;
        """
        )

        layout.addWidget(text1)
        layout.addWidget(text2)
        layout.addWidget(self.buttonBox)

        self.setStyleSheet(
            """QLabel{
            font-size: 12pt;
        }"""
        )
        self.setWindowTitle("Simple web browser")
        self.setLayout(layout)

