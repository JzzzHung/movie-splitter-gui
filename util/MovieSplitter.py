import cv2
from util.mThread import mThread
from util.mFile import mFile

class MovieSplitter(mThread, mFile):

    def __init__(self, filePath, frameRate, count, launchType):

        # init
        super().__init__()
        self.filePath = filePath
        self.frameRate = frameRate
        self.count = count
        self.COUNT = count
        self.launchType = launchType

        # prepare
        self.setFilePath(filePath)
        self.checkDir()

        # start
        self.vidcap = cv2.VideoCapture(self.filePath)
        self.setImageCount()


    def setImageCount(self):

        # calculate
        frames = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        self.seconds = round(frames / fps)

        # check frameRate
        if self.frameRate > 0:
            self.imgCount = round(self.seconds / self.frameRate)
        elif self.frameRate == -1: # get all frame of video
            self.imgCount = round(frames) - 1
            self.frameRate = round(1 / fps, 2)
        else:
            self.imgCount = 0
            self.trigger.emit('[ERROR] frameRate error', 0)
            print('[ERROR] frameRate error')

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

    def getMovieDuration(self):
        return self.seconds

    def run(self):

        # emit: {video} has {imgCount} image
        self._emitTitle(self.imgCount)

        sec = 0
        for _ in range(self.imgCount + 1):

            # get frame
            self.getFrame(sec)

            # next
            sec += self.frameRate
            sec = round(sec, 2)
            self.count += 1

            # emit: \r splitting {self.count}
            self._emitSplitting()

        self.count = self.COUNT
        self.vidcap.release()

        # emit: DONE
        self._emitDone()

    # ---------- EMIT ----------

    def _emitTitle(self, imgCount):
        self.trigger.emit(f'---------- {self.fname} Splitting ----------\n[{imgCount+1} image]', 0)
        self.trigger.emit('', 0)
        print(f'---------- {self.fname} ----------')
        print(f'{imgCount+1} image')

    def _emitSplitting(self):
        self.trigger.emit(f'splitting {self.count}', 1)
        print(f'\rsplitting {self.count}', end='')

    def _emitDone(self):
        self.trigger.emit(f'---------- DONE ----------\n', 0)
        print(f'\n---------- DONE ----------\n')

    def _emitProcesing(self):
        _counter = 0
        # TODO: set range in movie duration (self.seconds)
        for _ in range(10):
            self.trigger.emit(f'{_counter}', 1)
            # print(f'{_counter}')
            if self.ec.isFinished():
                print('----------------- FIN. -----------------')
                break
            _counter += 1
            time.sleep(1)