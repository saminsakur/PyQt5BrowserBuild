from PyQt5.QtWidgets import QMessageBox


class fileErrorDialog(QMessageBox):
    def __init__(self, *args, **kwargs):
        super(fileErrorDialog, self).__init__(*args, **kwargs)

        self.setText("Wrong file entered, Enter a correct file and try again.")
        self.setIcon(QMessageBox.Critical)

        self.setWindowTitle("Please enter a correct file")
        self.show()


class errorMsg(QMessageBox):
    def __init__(self, text: str = "An internal error occurred!"):
        super(errorMsg, self).__init__()

        self.setText(text)
        self.setIcon(QMessageBox.Critical)

        self.setWindowTitle("Error!")
        self.show()
