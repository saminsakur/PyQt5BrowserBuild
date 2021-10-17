from PyQt5.QtCore import QObject, pyqtSlot, QEventLoop, QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtWidgets import QDialog, QProgressDialog, QProgressBar


class PrintHandler(QObject):
    def __init__(self, parent=None):
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
                painter.drawText(
                    QPointF(10, 25), "We could not generate print preview."
                )
                painter.end()
