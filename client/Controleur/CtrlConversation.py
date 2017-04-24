import Tkinter
import time

from client.Controleur.Ctrl import Ctrl
from client.UI.ConversationUI import ConversationUI
from client.UI.RecevoirUI import RecevoirUI


class CtrlConversation(Ctrl):
    def __init__(self, parent, interlocuteur, tk, fromMainThread):
        self.interlocuteur = interlocuteur
        self.conversationUI = ConversationUI(self.envoyer,self.raccrocher,interlocuteur,tk, fromMainThread)
        Ctrl.__init__(self, parent)

    def raccrocher(self):
        self.parent.raccrocher(True)
        self.quit()

    def envoyer(self):
        message = self.conversationUI.getMessage()
        self.conversationUI.ajouterMessage("Vous: " + message)
        self.parent.envoyerMessage(message)

    def recevoirMessage(self,message):
        self.conversationUI.ajouterMessage(str(self.interlocuteur.numTel) + ": "+ message)

    def backgroundAction(self):
        pass

    def start(self):
        self.conversationUI.show()

    def quit(self):
        print "quitting"
        self.conversationUI.top.destroy()

