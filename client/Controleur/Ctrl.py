# coding=utf-8
import abc
from threading import Thread


class Ctrl:
    def __init__(self, parent):
        self.parent = parent
        self.doAsync()


    def doAsync(self):
        self.secondThread = Thread(target=self.backgroundAction)
        self.secondThread.start()

    @abc.abstractmethod
    def backgroundAction(self):
        """"Action a effectuer en fond. Attention: lancer l'UI après"""
