import cv2
from util.mThread import mThread
from util.mFile import mFile

class MovieSplitter(mThread, mFile):

    def __init__(self, filePathList, frameRate, count):
        super().__init__()
        self.filePathList = filePathList
        self.frameRate = frameRate
        self.count = count
        self.COUNT = count

    def getImageCount(self):

        # calculate
        frames = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        seconds = round(frames / fps)

        # check frameRate
        if self.frameRate > 0:
            imgCount = round(seconds / self.frameRate)
        elif self.frameRate == -1: # get all frame of video
            imgCount = round(frames) - 1
            self.frameRate = round(1 / fps, 2)
        else:
            imgCount = 0
            print('[ERROR] frameRate error')
        return imgCount

    def getFrame(self, sec):
        self.vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
        hasFrames, image = self.vidcap.read()
        if hasFrames:
            outputFname = self.setImgName(self.count)
            # cv2.imwrite(outputFname, image)
            # @REF https://cloud.tencent.com/developer/article/1667009
            cv2.imencode('.jpg', image)[1].tofile(outputFname) # save img from RAM
        else:
            print("<<< This Frame doesn't exist! >>>")

    def run(self):
        for f in self.filePathList:
            self.setFilePath(f)
            self.checkDir()
            self._do()

    def _do(self):

        # start
        self.vidcap = cv2.VideoCapture(self.filePath)
        imgCount = self.getImageCount()

        # emit: {video} has {imgCount} image
        self._emitTitle(imgCount)

        sec = 0
        for _ in range(imgCount+1):

            # get frame
            self.getFrame(sec)

            # next
            sec += self.frameRate
            sec = round(sec, 2)
            self.count += 1

            # emit: \r splitting {self.count}
            self._emitSplitting()

        self.count = self.COUNT

        # emit: DONE
        self._emitDone()

    # def __del__(self):
    #     super().__del__()
    #     self.vidcap.release()

    # ---------- EMIT ----------

    def _emitTitle(self, imgCount):
        self.trigger.emit(f'---------- {self.fname} ----------\n[{imgCount+1} image]', 0)
        self.trigger.emit('', 0)
        print(f'---------- {self.fname} ----------')
        print(f'{imgCount+1} image')

    def _emitSplitting(self):
        self.trigger.emit(f'splitting {self.count}', 1)
        print(f'\rsplitting {self.count}', end='')

    def _emitDone(self):
        self.trigger.emit(f'---------- DONE ----------\n', 0)
        print(f'\n---------- DONE ----------\n')