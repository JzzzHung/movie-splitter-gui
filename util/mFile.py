from pathlib import Path

class mFile():

    # [Architecture]

    # ** Video **
    # filePathList
    # └─filePath
    #   └─parent
    #   └─fname

    # ** Img **
    # outputDir = {parent}/{fname}
    # imgname = {outputDir}/{count}

    # filePath == path and file name
    def setFilePath(self, filePath):
        self.filePath = filePath
        p = Path(filePath)
        self.fname = p.stem
        self.outputDir = Path.joinpath(p.parent, self.fname)

    def checkDir(self):
        if not Path.exists(self.outputDir):
            Path.mkdir(self.outputDir)

    def setImgName(self, count):
        return str(Path.joinpath(self.outputDir, f'{count}.jpg'))