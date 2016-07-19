from tkinter import Entry

class TextField(Entry):

    def __init__(self, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        self.state = "normal"

    def setStateNormal(self):
        self.state = "normal"
        self.configure(state=self.state)

    def setStateReadonly(self):
        self.state = "readonly"
        self.configure(state=self.state)

    def setText(self, text):
        self.configure(state="normal")
        self.delete(0, len(self.get()))
        self.insert(0, text)
        self.configure(state=self.state)

    def getText(self):
        return self.get()