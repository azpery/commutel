# coding=utf-8
import Tkinter

from client.UI import UI


class ComposerUI(UI.UI):

    def __init__(self, actionComposer, tk):
        UI.UI.__init__(self, tk)

        self.actionComposer = actionComposer
        welcomeLabel = Tkinter.Label(self.top, text="Bienvenue sur CommuTel")
        welcomeLabel.pack()

        self.statut = Tkinter.Label(self.top, text="Vous êtes ")
        self.statut.pack()

        self.numLabel = Tkinter.Label(self.top, text="")
        self.numLabel.pack()

        L1 = Tkinter.Label(self.top, text="Numéro de téléphone")
        L1.pack()

        self.inputText = Tkinter.Entry(self.top, bd=5)
        self.inputText.pack()

        self.btnComposer = Tkinter.Button(self.top, text="Composer le numéro de téléphone", command=actionComposer)
        self.btnComposer.pack()

    def show(self):
        self.top.resizable(width=False, height=False)
        self.top.geometry('{}x{}'.format( 300, 200))
        self.top.mainloop()

    def isNumeroValide(self):
        numero = self.getNumeroCompose()
        print "Num saisi" +str(numero)+ "Taille numéro saisi: " +str(str(numero).__len__()) + " et est digit:" +str(str(numero).isdigit())
        return str(numero).__len__() == 10 and str(numero).isdigit()

    def getNumeroCompose(self):
        return self.inputText.get()

    def updateNumeroTelephoneUtilisateur(self, numTel):
        self.numLabel.configure( text="Votre numéro :" + str(numTel))

    def updateStatut(self, statut):
        self.statut.configure( text="Vous êtes " + statut)
