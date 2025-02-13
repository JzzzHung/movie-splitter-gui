from PyQt5.QtCore import QThread, pyqtSignal

class mThread(QThread):

    trigger = pyqtSignal(str, int)

    def __init__(self):
        super(mThread, self).__init__()
