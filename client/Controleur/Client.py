# coding=utf-8
import Tkinter
import time
from Queue import Queue

from client.Controleur.CtrlCommunication import CtrlCommunication
from client.Controleur.CtrlComposition import CtrlComposition
from client.Controleur.CtrlConversation import CtrlConversation
from client.Controleur.CtrlRecevoir import CtrlRecevoir
from client.Model.Statut import statut
from client.Model.Utilisateur import Utilisateur
from client.UI.UI import UI


class Client:
    def __init__(self):
        self.me = Utilisateur()
        self.statut = statut.UNREGISTRED
        self.queue = Queue()
        self.top = Tkinter.Tk()
        self.top.after(100, self.read_queue)
        self.ctrlCommunication = CtrlCommunication(self)
        self.ctrlComposition = CtrlComposition(self, self.top)
        self.ctrlComposition.start()

    def composerNumeroTelephone(self, numTel):
        if self.statut == statut.READY_FOR_CONVERSATION:
            self.updateStatut(statut.COMPOSING)
            self.interlocuteur = Utilisateur()
            self.interlocuteur.numTel = numTel
            self.ctrlCommunication.composerNumeroTelephone(numTel)
        else:
            UI.printMessageBox("Info","Composition du numéro en court")

    def read_queue(self):
        try:
            items = self.queue.get_nowait()
            func = items[0]
            args = items[1:]
            func(*args)
        except:
            pass
        self.top.after(100, self.read_queue)

    def updateNumeroTelephoneUtilisateur(self,numTel):
        print "Mise à jour numéro de téléphone: "+numTel
        self.me.numTel = numTel
        self.updateStatut(statut.READY_FOR_CONVERSATION)
        self.ctrlComposition.updateNumeroTelephoneUtilisateur(numTel)

    def destinataireOccupe(self, t):
        UI.printMessageBox("Destinataire occupé", "Votre destinataire est actuellement occupé")
        self.updateStatut(statut.READY_FOR_CONVERSATION)

    def destinataireInexistant(self, t):
        UI.printMessageBox("Destinataire inexistant", "Le numéro que vous avez composé n'est pas attribué.")
        self.updateStatut(statut.READY_FOR_CONVERSATION)


    def updateStatut(self, s):
        print "Changement de statut:" + str(statut)
        if s == statut.READY_FOR_CONVERSATION or statut == statut.CONNECTION_OK:
            self.ctrlComposition.composerUI.updateStatut("en ligne")
        elif s == statut.BUSY:
            self.ctrlComposition.composerUI.updateStatut("occupé")
        elif s == statut.COMPOSING:
            self.ctrlComposition.composerUI.updateStatut("en train de composer un numéro")
        elif s == statut.PENDING:
            self.ctrlComposition.composerUI.updateStatut("occupé")
        self.statut = s

    def demandeCommunication(self, numeroInterlocuteur):
        print "Demande de communication de : " + str(numeroInterlocuteur)
        if self.statut == statut.READY_FOR_CONVERSATION:
            self.updateStatut(statut.PENDING)
            self.interlocuteur = Utilisateur()
            self.interlocuteur.numTel = numeroInterlocuteur
            self.ctrlRecevoir = CtrlRecevoir(self,self.interlocuteur, self.top)
        else:
            self.ctrlCommunication.envoyerReponseDemandeCommunication(statut.BUSY)

    def decrocher(self, t):

        print "Décrochage"
        self.ctrlCommunication.envoyerReponseDemandeCommunication(statut.READY_FOR_CONVERSATION)
        self.ctrlRecevoir.quit()
        self.demarrerConversation(True)

    def endTimeOut(self):
        self.ctrlCommunication.envoyerReponseDemandeCommunication(statut.TIME_OUT)
        self.ctrlRecevoir.quit()



    def demarrerConversation(self, fromMainThread):
        self.updateStatut(statut.BUSY)
        self.ctrlConversation = CtrlConversation(self,self.interlocuteur, self.ctrlComposition.composerUI.top, fromMainThread)

    def envoyerMessage(self, message):
        self.ctrlCommunication.envoyerMessage(message)

    def recevoirMessage(self, message):
        self.ctrlConversation.recevoirMessage(message)

    def raccrocher(self, t):
        self.ctrlCommunication.raccrocher()
        self.updateStatut(statut.READY_FOR_CONVERSATION)
        self.ctrlConversation.quit()