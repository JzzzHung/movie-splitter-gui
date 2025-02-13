import ffmpeg
from util.mThread import mThread
from pathlib import Path
import time

class Encoder(mThread):
    def __init__(self, filePath, movieDuration):
        super().__init__()
        self.fInput = filePath
        self.setOutputFilePath(filePath)
        self.sec = movieDuration

    def setOutputFilePath(self, filePath):
        p = Path(filePath)
        self.fname = p.stem
        # p.stem: file name without '.mp4'
        # p.name: file name with '.mp4'
        self.fOutput = str(Path.joinpath(p.parent, p.stem, p.name))

    def run(self):
        # self.fInput = "C:/Videos/a.mp4"
        # self.fOutput = "C:/Videos/a/a.mp4"
        (ffmpeg
            .input(self.fInput)
            .output(self.fOutput)
            .global_args('-hide_banner')
            .run(overwrite_output=True))

    def getNewFilePath(self):
        return self.fOutput

    def _emitProcessing(self):
        counter = 0
        while True:

            # Processing time
            formatedTime = time.strftime("%H:%M:%S",time.gmtime(counter))

            if counter < self.sec:
                self.trigger.emit(f'---------- {self.fname} Re-encoding ----------\n{formatedTime}', 1)
            else:
                # If re-encoding time gratter than movie duration, remind user to see terminal (ffmpeg log)
                self.trigger.emit(f'---------- {self.fname} Re-encoding ----------\n{formatedTime}\nPlease check terminal.', 1)
            if self.isFinished():
                self.trigger.emit('', 0)
                self.trigger.emit(f'-------------- Re-encode DONE --------------', 1)
                print('-------------- Re-encode DONE --------------')
                break
            counter += 1
            time.sleep(1)