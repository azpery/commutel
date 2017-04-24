# coding=utf-8
import time

from client.Controleur.Ctrl import Ctrl
from client.UI.RecevoirUI import RecevoirUI


class CtrlRecevoir(Ctrl):
    def __init__(self, parent, interlocuteur, tk):
        self.stop = False
        self.recevoirUI = RecevoirUI(self.decrocher, interlocuteur, tk)
        Ctrl.__init__(self, parent)

    def decrocher(self):
        self.parent.queue.put((self.parent.decrocher, True))

    def backgroundAction(self):
        for t in range(60, -1, -1):
            if not self.stop:
                seconds = t % 60
                self.recevoirUI.updateTimeLeft(seconds)
                time.sleep(1.0)

    def start(self):
        self.recevoirUI.show()

    def quit(self):
        self.recevoirUI.destroy()
        self.stop = True

