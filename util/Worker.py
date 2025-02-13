from util.mThread import mThread
from util.MovieSplitter import MovieSplitter
from util.Encoder import Encoder
from enum import Enum

class WorkEnum(Enum):
    START = 1
    RE_ENCODE = 2

class Worker(mThread):
    def __init__(self, filePathList, frameRate, count, launchType, display):
        super().__init__()
        self.filePathList = filePathList
        self.frameRate = frameRate
        self.count = count
        self.launchType = launchType
        self.display = display

    def run(self):
        for filePath in self.filePathList:
            # @REF https://blog.csdn.net/chengmo123/article/details/96477103
            self.ms = MovieSplitter(filePath, self.frameRate, self.count, self.launchType)
            self.ms.trigger.connect(self.display) # LISTENING

            if self.launchType == WorkEnum.RE_ENCODE:

                # Start
                self.ec = Encoder(filePath, self.ms.getMovieDuration())
                self.ec.trigger.connect(self.display) # LISTENING
                self.ec.start()

                # Processing
                self.ec._emitProcessing()
                self.ec.wait()

                # Done
                self.ms.filePath = self.ec.getNewFilePath()

            self.ms.start()
            self.ms.wait()
