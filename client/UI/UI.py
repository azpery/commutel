import Tkinter
import tkMessageBox
from Tkinter import *

class UI:
    def __init__(self):
        self.top = Tkinter.Tk()

    @staticmethod
    def printMessageBox(title, message):
        tkMessageBox.showinfo(title, message)