# coding=utf-8
import time

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
        self.ctrlCommunication = CtrlCommunication(self)
        self.ctrlComposition = CtrlComposition(self)
        self.ctrlComposition.start()

    def composerNumeroTelephone(self, numTel):
        if self.statut == statut.READY_FOR_CONVERSATION:
            self.updateStatut(statut.COMPOSING)
            self.interlocuteur = Utilisateur()
            self.interlocuteur.numTel = numTel
            self.ctrlCommunication.composerNumeroTelephone(numTel)
        else:
            UI.printMessageBox("Info","Composition du numéro en court")

    def updateNumeroTelephoneUtilisateur(self,numTel):
        print "Mise à jour numéro de téléphone: "+numTel
        self.me.numTel = numTel
        self.updateStatut(statut.READY_FOR_CONVERSATION)
        self.ctrlComposition.updateNumeroTelephoneUtilisateur(numTel)

    def updateStatut(self, statut):
        print "Changement de statut:" + str(statut)
        self.statut = statut

    def demandeCommunication(self, numeroInterlocuteur):
        print "Demande de communication de : " + str(numeroInterlocuteur)
        if self.statut == statut.READY_FOR_CONVERSATION:
            self.updateStatut(statut.PENDING)
            self.interlocuteur = Utilisateur()
            self.interlocuteur.numTel = numeroInterlocuteur
            self.ctrlRecevoir = CtrlRecevoir(self,self.interlocuteur)
        else:
            self.ctrlCommunication.envoyerReponseDemandeCommunication(statut.BUSY)

    def decrocher(self):
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

    def raccrocher(self):
        self.ctrlCommunication.raccrocher()
        self.updateStatut(statut.READY_FOR_CONVERSATION)
        self.ctrlConversation.quit()