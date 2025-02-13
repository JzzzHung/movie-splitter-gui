import sys
from PyQt5.QtWidgets import QApplication
from view.ui import MainWindow
from util.MovieSplitter import MovieSplitter

class Main(MainWindow):
    def __init__(self):
        super().__init__()
        self.initBtn()
        self.initPlay()

    def initBtn(self):
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.btnClear.clicked.connect(self.btnClearClicked)

    # Splitter Thread
    def btnStartClicked(self):
        frameRate = float(self.lineeditFrameRate.text())
        count = int(self.lineeditCount.text())
        filePathList = self.textEdit.filePathList

        if len(filePathList) == 0:
            self.play()
        else:
            # @REF https://blog.csdn.net/chengmo123/article/details/96477103
            self.ms = MovieSplitter(frameRate, count)
            self.ms.setFilePathList(filePathList)
            self.ms.trigger.connect(self.display) # LISTENING
            self.ms.start()
            self.counter = 0

    def btnClearClicked(self):
        self.textEdit.filePathList.clear()
        self.textEdit.setText('')

    def display(self, msg, goLineStart):
        if goLineStart:
            self.listwidgetOutput.setCurrentRow(self.listwidgetOutput.count() - 1)
            self.listwidgetOutput.takeItem(self.listwidgetOutput.currentRow())
        self.listwidgetOutput.addItem(msg)
        self.listwidgetOutput.scrollToBottom()

    def initPlay(self):
        self.counter = 0
        self.playList = [
            'There is no video to split.',
            'There is no video to split! Please select at least one video.',
            'NO VIDEO LA!!!',
            '(╯°Д°)╯ ┻┻',
            "┳┳ ╭( ' - '╭)"
                         ]

    def play(self):
        if self.counter < 3:
            self.display(self.playList[self.counter], 0)
        else:
            if self.counter % 2 != 0:
                # @REF https://facemood.grtimed.com/classification/%E6%86%A4%E6%80%92
                self.display(self.playList[3], 0)
            else:
                # @REF https://facemood.grtimed.com/classification/%E7%84%A1%E5%A5%88
                # @REF https://www.compart.com/en/unicode/U+256D
                self.display(self.playList[4], 0)
        self.counter += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())