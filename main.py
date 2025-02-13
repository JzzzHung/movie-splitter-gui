import sys
from PyQt5.QtWidgets import QApplication
from view.ui import MainWindow
from util.mPlay import mPlay
from util.Worker import Worker
from util.Worker import WorkEnum

class Main(MainWindow):
    def __init__(self):
        super().__init__()
        self.initBtn()
        self.player = mPlay(self.display)

    def initBtn(self):
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.btnClear.clicked.connect(self.btnClearClicked)
        self.btnReencode.clicked.connect(self.btnReencodeClicked)

    # Splitter Thread
    def btnStartClicked(self):
        self.launch(WorkEnum.START)

    # Re-encode Thread
    def btnReencodeClicked(self):
        self.launch(WorkEnum.RE_ENCODE)

    def launch(self, launchType):
        filePathList, frameRate, count = self.getParams()
        if len(filePathList) == 0:
            self.player.play()
        else:
            self.wocker = Worker(filePathList, frameRate, count, launchType, self.display)
            self.wocker.start()
            self.player.resetCounter()

    def getParams(self):
        filePathList = self.textEdit.filePathList
        frameRate = float(self.lineeditFrameRate.text())
        count = int(self.lineeditCount.text())
        return filePathList, frameRate, count

    def btnClearClicked(self):
        self.textEdit.filePathList.clear()
        self.textEdit.setText('')

    def display(self, msg, goLineStart):
        if goLineStart:
            self.listwidgetOutput.setCurrentRow(self.listwidgetOutput.count() - 1)
            self.listwidgetOutput.takeItem(self.listwidgetOutput.currentRow())
        self.listwidgetOutput.addItem(msg)
        self.listwidgetOutput.scrollToBottom()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())