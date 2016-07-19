from tkinter import *
from tkinter.filedialog import askopenfilename
from Settings import Settings
from ui.TextField import TextField
import cv2


class LoadWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        Label(self, text="Moviefile").grid(row=0, column=0, sticky=W, pady=10)
        Label(self, text="FrameWidth").grid(row=1, column=0, sticky=W, pady=10)
        Label(self, text="FrameHeight").grid(row=2, column=0, sticky=W, pady=10)
        Label(self, text="Frames").grid(row=3, column=0, sticky=W, pady=10)
        Label(self, text="OutputWidth").grid(row=4, column=0, sticky=W, pady=10)
        Label(self, text="OutputHeight").grid(row=5, column=0, sticky=W, pady=10)
        Label(self, text="LabelWidth").grid(row=6, column=0, sticky=W, pady=10)
        Label(self, text="LabelHeight").grid(row=7, column=0, sticky=W, pady=10)
        Label(self, text="Nr of frames").grid(row=8, column=0, sticky=W, pady=10)

        self.moviefileInput = TextField(self)
        self.moviefileInput.grid(row=0, column=1, sticky=N + E + S + W, pady=10, padx=20)
        self.moviefileInput.setText("?")
        self.moviefileInput.setStateReadonly()

        self.frameWidthInput = TextField(self)
        self.frameWidthInput.grid(row=1, column=1, sticky=N + E + S + W, pady=10, padx=20)
        self.frameWidthInput.setText("0")
        self.frameWidthInput.setStateReadonly()

        self.frameHeightInput = TextField(self)
        self.frameHeightInput.grid(row=2, column=1, sticky=N + E + S + W, pady=10, padx=20)
        self.frameHeightInput.setText("0")
        self.frameHeightInput.setStateReadonly()

        self.framesInput = TextField(self)
        self.framesInput.grid(row=3, column=1, sticky=N + E + S + W, pady=10, padx=20)
        self.framesInput.setText("0")
        self.framesInput.setStateReadonly()

        self.outputWidthInput = TextField(self)
        self.outputWidthInput.grid(row=4, column=1, sticky=N + E + S + W, pady=10, padx=20)

        self.outputHeightInput = TextField(self)
        self.outputHeightInput.grid(row=5, column=1, sticky=N + E + S + W, pady=10, padx=20)

        self.labelWidthInput = TextField(self)
        self.labelWidthInput.grid(row=6, column=1, sticky=N + E + S + W, pady=10, padx=20)

        self.labelHeightInput = TextField(self)
        self.labelHeightInput.grid(row=7, column=1, sticky=N + E + S + W, pady=10, padx=20)

        self.nrFramesInput = TextField(self)
        self.nrFramesInput.grid(row=8, column=1, sticky=N + E + S + W, pady=10, padx=20)

        self.movieChooseButton = Button(self, text="Choose", command=self.onMovieChooseClick)
        self.movieChooseButton.grid(row=0, column=2, sticky=N + E + S + W, pady=10)

        Label(self, text="px").grid(row=4, column=2, sticky=W, pady=10)
        Label(self, text="px").grid(row=5, column=2, sticky=W, pady=10)
        Label(self, text="px").grid(row=6, column=2, sticky=W, pady=10)
        Label(self, text="px").grid(row=7, column=2, sticky=W, pady=10)

        self.loadButton = Button(self, text="Load", command=self.onLoadClick)
        self.loadButton.grid(row=9, column=0, columnspan=3, sticky=N + E + S + W)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)

    def onLoadClick(self):
        if self.framesInput.getText() != "0":
            Settings.movieFile = self.moviefileInput.get()
            Settings.frameWidth = int(self.frameWidthInput.get())
            Settings.frameHeight = int(self.frameHeightInput.get())
            Settings.frames = int(self.framesInput.get())

            Settings.outputWidth = int(self.outputWidthInput.get())
            Settings.outputHeight = int(self.outputHeightInput.get())

            Settings.labelWidth = int(self.labelWidthInput.get())
            Settings.labelHeight = int(self.labelHeightInput.get())

            Settings.nrFrames = int(self.nrFramesInput.getText())

            self.controller.createWorkingWindow()


    def onMovieChooseClick(self):
        file = askopenfilename(filetypes=[("Movie", "*.mp4")])

        if file is not None and file != '':
            cap = cv2.VideoCapture(file)

            imageWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            imageHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            imageCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            cap.release()

            self.moviefileInput.setText(file)

            self.frameWidthInput.setText(imageWidth)
            self.frameHeightInput.setText(imageHeight)
            self.framesInput.setText(imageCount)

            self.outputWidthInput.setText(int(imageWidth/8))
            self.outputHeightInput.setText(int(imageHeight/8))

            self.labelWidthInput.setText(int(imageWidth/8))
            self.labelHeightInput.setText(int(imageHeight/8))

            self.nrFramesInput.setText(10)