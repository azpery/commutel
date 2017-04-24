# coding=utf-8
from client.Controleur.Ctrl import Ctrl
from client.UI.ComposerUI import ComposerUI
from client.UI.UI import UI


class CtrlComposition(Ctrl):

    def __init__(self, parent, tk):
        self.composerUI = ComposerUI(self.composer, tk)
        Ctrl.__init__(self, parent)

    def start(self):
        self.composerUI.show()

    def backgroundAction(self):
        pass

    def composer(self):
        numTel = self.composerUI.getNumeroCompose()
        if(self.composerUI.isNumeroValide()):
            print "Numéro de télephone composé: " + numTel
            self.parent.composerNumeroTelephone(numTel)
        else:
            UI.printMessageBox("Mauvais numéro", "Veuillez vérifier le numéro saisi")

    def updateNumeroTelephoneUtilisateur(self,numTel):
        self.composerUI.updateNumeroTelephoneUtilisateur(numTel)
