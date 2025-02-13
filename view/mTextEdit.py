from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont

class mTextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.initProperty()
        self.initStyle()
        self.filePathList = []

    def initProperty(self):
        self.setAcceptDrops(True)
        # self.setReadOnly(True)

    def initStyle(self):
        self.setFont(QFont('PMingLiU', 16))

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.getFilePathList(e.mimeData().urls())
        fileList = self.getFileList()
        self.setText(fileList)

    def getFilePathList(self, pathes):
        for f in pathes:
            if f.toLocalFile() not in self.filePathList:
                self.filePathList.append(f.toLocalFile())
        self.filePathList.sort()

    # just get file name
    def getFileList(self):
        result = [f.split('/')[-1] for f in self.filePathList]
        return '\n'.join(result)