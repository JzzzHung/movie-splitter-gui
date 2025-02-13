import ffmpeg
from util.mThread import mThread
from pathlib import Path

class Encoder(mThread):
    def __init__(self, filePath):
        super().__init__()
        self.fInput = filePath
        self.setOutputFilePath(filePath)

    def setOutputFilePath(self, filePath):
        p = Path(filePath)
        # p.stem: file name without '.mp4'
        # p.name: file name with '.mp4'
        self.fOutput = str(Path.joinpath(p.parent, p.stem, p.name))

    def run(self):
        print(self.fInput)
        print(self.fOutput)
        # self.fInput = "C:/Videos/a.mp4"
        # self.fOutput = "C:/Videos/a/a.mp4"
        ffmpeg.input(self.fInput).output(self.fOutput).run(overwrite_output=True)

    def getNewFilePath(self):
        return self.fOutput