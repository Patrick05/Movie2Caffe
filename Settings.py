class Settings:

    movieFile = ""

    frameWidth = 100
    frameHeight = 50
    frames = 0

    outputWidth = 100
    outputHeight = 50

    labelWidth = 50
    labelHeight = 25

    nrFrames = 10

    @staticmethod
    def getOutputLabelFactors():
        return float(Settings.labelWidth)/float(Settings.outputWidth), float(Settings.labelHeight)/float(Settings.outputHeight)