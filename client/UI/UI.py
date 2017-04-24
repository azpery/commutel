import Tkinter
import tkMessageBox

class UI:
    def __init__(self, tk):
        self.top = tk

    @staticmethod
    def printMessageBox(title, message):
        tkMessageBox.showinfo(title, message)