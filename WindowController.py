from tkinter import Tk, Frame
from LoadWindow import LoadWindow
from WorkingWindow import WorkingWindow

class Controller(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        self.loadWindow = LoadWindow(self.container, self)
        self.loadWindow.grid(row=0, column=0, sticky="nesw")

        self.showLoadWindow()

    def showLoadWindow(self):
        self.loadWindow.tkraise()

    def createWorkingWindow(self):
        workingWindow = WorkingWindow(self.container, self)
        workingWindow.grid(row=0, column=0, sticky="nesw")
        workingWindow.tkraise()