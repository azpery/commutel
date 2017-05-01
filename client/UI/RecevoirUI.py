# coding=utf-8
import Tkinter

from client.UI import UI


class RecevoirUI:

    def __init__(self, actionDecrocher, interlocuteur, tk):
        self.top = Tkinter.Toplevel(tk)
        self.interlocuteur = interlocuteur
        self.actionDecrocher = actionDecrocher
        appelLabel = Tkinter.Label(self.top, text="Appel entrant")
        appelLabel.pack()

        self.numLabel = Tkinter.Label(self.top, text="Votre interlocuteur : " + str(interlocuteur.numTel))
        self.numLabel.pack()

        self.timeLeftLabel = Tkinter.Label(self.top, text="")
        self.timeLeftLabel.pack()

        self.btnDecrocher = Tkinter.Button(self.top, text="Décrocher", command=actionDecrocher)
        self.btnDecrocher.pack()

    def show(self):
        self.top.resizable(width=False, height=False)
        self.top.geometry('{}x{}'.format( 300, 200))
        self.top.mainloop()

    def updateTimeLeft(self, timeLeft):
        self.timeLeftLabel.configure(text="Temps restant: " + str(timeLeft) + " secondes")

    def destroy(self):
        self.top.destroy()

