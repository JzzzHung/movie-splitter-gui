from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from view.mTextEdit import mTextEdit

UI_Path = "./view/ui.ui"

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi(UI_Path,self)
        self.initLineEdit()
        self.initTextEdit()
        self.initListWidget()

    def initLineEdit(self):
        self.lineeditFrameRate.setText(str(30))
        self.lineeditCount.setText(str(0))
        self.lineeditFrameRate.setValidator(QDoubleValidator()) # only double number valid
        self.lineeditCount.setValidator(QIntValidator()) # only int number valid

    def initTextEdit(self):
        self.textEdit = mTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(30, 70, 470, 260))
        self.textEdit.setPlaceholderText('Drag and Drop Files Here.')

    def initListWidget(self):
        self.listwidgetOutput.setFocus()
        # self.listwidgetOutput.setFont(QFont('PMingLiU', 16))