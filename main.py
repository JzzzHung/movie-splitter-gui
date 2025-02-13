import sys
from PyQt5.QtWidgets import QApplication
from view.ui import MainWindow
from util.MovieSplitter import MovieSplitter
from util.mplay import mPlay

class Main(MainWindow):
    def __init__(self):
        super().__init__()
        self.initBtn()
        self.player = mPlay(self.display)

    def initBtn(self):
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.btnClear.clicked.connect(self.btnClearClicked)

    # Splitter Thread
    def btnStartClicked(self):
        filePathList = self.textEdit.filePathList
        frameRate = float(self.lineeditFrameRate.text())
        count = int(self.lineeditCount.text())

        if len(filePathList) == 0:
            self.player.play()
        else:
            # @REF https://blog.csdn.net/chengmo123/article/details/96477103
            self.ms = MovieSplitter(filePathList, frameRate, count)
            self.ms.trigger.connect(self.display) # LISTENING
            self.ms.start()
            self.player.resetCounter()

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