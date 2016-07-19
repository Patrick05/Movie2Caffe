from tkinter import *
from Settings import Settings
from tkinter.ttk import Progressbar
import cv2
import numpy as np
from PIL import Image, ImageTk
import h5py

class WorkingWindow(Frame):

    STATE_NONE = 0
    STATE_CLICK = 1

    def __init__(self,  parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        self.frameCanvas = Label(self, width=Settings.outputWidth, height=Settings.outputHeight)
        self.frameCanvas.grid(row=0, column=0, columnspan=5, pady=10)
        self.frameCanvas.bind("<Button-1>", self.markPosition)

        self.labelCanvas = Label(self, width=Settings.labelWidth, height=Settings.labelHeight)
        self.labelCanvas.grid(row=0, column=5, pady=10)
        self.labelCanvas.bind("<Button-1>", self.unmarkPosition)

        self.prevButton = Button(self, text="<<", command=self.showPrev)
        self.prevButton.grid(row=1, column=0, sticky="nesw")

        self.saveButton = Button(self, text="Save", command=self.save)
        self.saveButton.grid(row=1, column=2, sticky="nesw")

        self.nextButton = Button(self, text=">>", command=self.showNext)
        self.nextButton.grid(row=1, column=4, sticky="nesw")

        self.progressBar = Progressbar(self, orient=HORIZONTAL)
        self.progressBar.grid(row=2, column=0, columnspan=5, sticky="nesw", pady=10)

        self.stateLabel = Label(self, text="Loading...")
        self.stateLabel.grid(row=3, column=0, pady=10)

        self.frames = []
        self.labels = []
        self.currentFrame = 0

        self.loadVideo()
        self.showCurrentFrame()

        self.clickedPos = (0,0)
        self.drawState = WorkingWindow.STATE_NONE


    def loadVideo(self):
        file = Settings.movieFile

        cap = cv2.VideoCapture(file)
        index = 0
        while cap.isOpened() and index < Settings.nrFrames:
            ret, frame = cap.read()

            if frame is None:
                break
            else:
                self.frames.append(
                    cv2.cvtColor(
                        cv2.resize(
                            frame,
                            (int(Settings.outputWidth), int(Settings.outputHeight))
                        ),
                        cv2.COLOR_BGR2RGBA
                    )
                )
                self.labels.append(
                    cv2.cvtColor(
                        np.zeros(
                            (int(Settings.labelHeight), int(Settings.labelWidth), 1),
                            np.uint8
                        ),
                        cv2.COLOR_GRAY2RGBA
                    )
                )
            index += 1


    def showCurrentFrame(self):
        image = Image.fromarray(self.frames[self.currentFrame])
        image2 = ImageTk.PhotoImage(image=image)
        self.frameCanvas.image = image2
        self.frameCanvas.configure(image=image2)

        label = Image.fromarray(self.labels[self.currentFrame])
        label2 = ImageTk.PhotoImage(image=label)
        self.labelCanvas.image = label2
        self.labelCanvas.configure(image=label2)

        self.stateLabel.configure(text=("Frame {} / {}".format(self.currentFrame, len(self.frames))))


    def showPrev(self):
        if self.currentFrame > 0:
            self.currentFrame -= 1
        self.updateButtons()
        self.showCurrentFrame()

    def showNext(self):
        if self.currentFrame + 1 < len(self.frames):
            self.currentFrame += 1
        self.updateButtons()
        self.showCurrentFrame()

    def updateButtons(self):
        if self.currentFrame <= 0:
            self.prevButton.configure(state="disable")
        else:
            self.prevButton.configure(state="normal")

        if self.currentFrame+1 >= len(self.frames):
            self.nextButton.configure(state="disabl")
        else:
            self.nextButton.configure(state="normal")

    def markPosition(self, event):
        wFactor, hFactor = Settings.getOutputLabelFactors()

        if self.drawState == WorkingWindow.STATE_NONE:
            self.clickedPos = (int(event.x * wFactor), int(event.y * hFactor))
            self.drawState = WorkingWindow.STATE_CLICK
            self.stateLabel.configure(text=("Frame {} / {} - Wfsp!".format(self.currentFrame, len(self.frames))))
        elif self.drawState == WorkingWindow.STATE_CLICK:
            cv2.rectangle(self.labels[self.currentFrame], self.clickedPos, (int(event.x * wFactor), int(event.y * hFactor)), (255,255,255), -1)
            self.drawState = WorkingWindow.STATE_NONE
            self.showNext()
           # self.showCurrentFrame()


    def unmarkPosition(self, event):
        cv2.circle(self.labels[self.currentFrame], (event.x, event.y), 8, (0, 0, 0, 255), -1)
        self.showCurrentFrame()

    def convertFrames(self):
        convertedFrames = []
        for index in range(0, self.currentFrame+1):
            convertedFrames.append(
                np.transpose(
                    self.frames[index].astype("float"),
                    (2,0,1)
                )
            )

            for x in range(0, convertedFrames[len(convertedFrames)-1].shape[1]):
                for y in range(0, convertedFrames[len(convertedFrames)-1].shape[2]):
                    for c in range(0, convertedFrames[len(convertedFrames)-1].shape[0]):
                        convertedFrames[len(convertedFrames)-1][c][x][y] = float(convertedFrames[len(convertedFrames)-1][c][x][y])/255.0

        return convertedFrames

    def convertLabels(self):
        convertedLabels = [] # todo convert to binary image
        for index in range(0, self.currentFrame+1):
            convertedLabels.append(
                cv2.cvtColor(
                    self.labels[index],
                    cv2.COLOR_RGBA2GRAY
                )
            )

            for x in range(0, convertedLabels[len(convertedLabels) - 1].shape[1]):
                for y in range(0, convertedLabels[len(convertedLabels) - 1].shape[2]):
                    convertedLabels[len(convertedLabels) - 1][0][x][y] = float(convertedLabels[len(convertedLabels) - 1][0][x][y])/255.0

        return convertedLabels


    def save(self):
        convertedFrames = self.convertFrames()
        convertedLabels = self.convertLabels()

        h5f = h5py.File("data.h5", "w")
        h5f.create_dataset("data", (self.currentFrame+1, 3, Settings.outputHeight, Settings.outputWidth))
        h5f.create_dataset("label", (self.currentFrame+1, 1, Settings.labelHeight, Settings.labelWidth))

        for index in range(0, self.currentFrame):
            h5f["data"] = convertedFrames[index]
            h5f["label"] = convertedLabels[index]

        h5f.close()