from pathlib import Path
import cv2
from util.mThread import mThread

class MovieSplitter(mThread):

    def __init__(self, frameRate, count):
        super().__init__()
        self.frameRate = frameRate
        self.count = count
        self.COUNT = count

    # def __del__(self):
    #     super().__del__()
    #     self.vidcap.release()

    def checkDir(self):
        if not Path.exists(self.outputDir):
            Path.mkdir(self.outputDir)

    def getImageCount(self):
        frames = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        seconds = round(frames / fps)
        imgCount = round(seconds / self.frameRate)
        if self.frameRate == -1:
            imgCount = round(frames) - 1
            self.frameRate = round(1 / fps, 2)
        return imgCount

    def getFrame(self, sec):
        self.vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
        hasFrames, image = self.vidcap.read()
        if hasFrames:
            outputFname = str(Path.joinpath(self.outputDir, f'{self.count}.jpg'))
            # cv2.imwrite(outputFname, image)
            # @REF https://cloud.tencent.com/developer/article/1667009
            cv2.imencode('.jpg', image)[1].tofile(outputFname) # save img from RAM
        else:
            print("<<< This Frame doesn't exist! >>>")

    # filePath == path and file name
    def setFilePath(self, filePath):
        self.filePath = filePath
        p = Path(filePath)
        self.fname = p.stem
        self.outputDir = Path.joinpath(p.parent, self.fname)

    def setFilePathList(self, filePathList):
        self.filePathList = filePathList

    def run(self):
        for f in self.filePathList:
            self.setFilePath(f)
            self.checkDir()
            self._do()

    def _do(self):
        self.vidcap = cv2.VideoCapture(self.filePath)
        imgCount = self.getImageCount() # emit: {video} has {imgCount} image

        # ↓↓↓↓ EMIT ↓↓↓↓ #
        self.trigger.emit(f'---------- {self.fname} ----------\n[{imgCount+1} image]', 0)
        self.trigger.emit('', 0)
        print(f'---------- {self.fname} ----------')
        print(f'{imgCount+1} image')
        # ↑↑↑↑ EMIT ↑↑↑↑ #

        sec = 0
        for _ in range(imgCount+1):

            # get frame
            self.getFrame(sec)  # emit: \r splitting {self.count}

            # next
            sec += self.frameRate
            sec = round(sec, 2)
            self.count += 1

            # ↓↓↓↓ EMIT ↓↓↓↓ #
            self.trigger.emit(f'splitting {self.count}', 1)
            print(f'\rsplitting {self.count}', end='')
            # ↑↑↑↑ EMIT ↑↑↑↑ #

        self.count = self.COUNT

        # ↓↓↓↓ EMIT ↓↓↓↓ #
        self.trigger.emit(f'---------- DONE ----------\n', 0)
        print(f'\n---------- DONE ----------\n')
        # ↑↑↑↑ EMIT ↑↑↑↑ #
