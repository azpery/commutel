# coding=utf-8
from client.Controleur.Ctrl import Ctrl
from client.Model.Command import command
from client.Model.Statut import statut
from client.Service.Api import Api
from client.UI.UI import UI
from client.Utils.Wrapper import Wrapper


class CtrlCommunication(Ctrl):
    def __init__(self, parent):
        Ctrl.__init__(self, parent)

    def composerNumeroTelephone(self, numTel):
        wrappedCommand = self.wrapper.wrapCommand(numTel)
        self.api.send(wrappedCommand)

    def envoyerReponseDemandeCommunication(self, statut):
        wrappedCommand = self.wrapper.wrapStatus(statut)
        self.api.send(wrappedCommand)

    def envoyerMessage(self, message):
        wrappedCommand = self.wrapper.wrapMessage(message)
        self.api.send(wrappedCommand)

    def raccrocher(self):
        wrappedCommand = self.wrapper.wrapStatus(statut.DISCONNECTED)
        self.api.send(wrappedCommand)

    def callback(self, data):
        print "callback : " + str( self.bucket.getNatureOfLastMessage())
        if self.bucket.getNatureOfLastMessage() == command.STATUS and self.parent.statut == statut.UNREGISTRED and int(
                self.bucket.getInnerMessage()) == statut.CONNECTION_OK:
            self.parent.updateStatut(statut.REGISTRED)
            print "Client connecte au terminal"
        elif self.bucket.getNatureOfLastMessage() == command.MESSAGE and self.parent.statut == statut.REGISTRED:
            self.parent.updateNumeroTelephoneUtilisateur(self.bucket.getInnerMessage())
        elif self.bucket.getNatureOfLastMessage() == command.ASK:
            self.parent.demandeCommunication(self.bucket.getInnerMessage())
        elif self.bucket.getNatureOfLastMessage() == command.MESSAGE and self.parent.statut == statut.BUSY:
            self.parent.recevoirMessage(self.bucket.getInnerMessage())
        elif self.bucket.getNatureOfLastMessage() == command.STATUS and int(
                self.bucket.getInnerMessage()) == statut.READY_FOR_CONVERSATION and self.parent.statut == statut.COMPOSING:
            print "debut conversation"
            self.parent.demarrerConversation(False)
        elif self.bucket.getNatureOfLastMessage() == command.STATUS and int(
                int(self.bucket.getInnerMessage())) == statut.DISCONNECTED and self.parent.statut == statut.BUSY:
            print "debut conversation"
            self.parent.raccrocher()

    #Implémentation méthode abstraite
    def backgroundAction(self):
        self.api = Api(self.callback)
        self.bucket = self.api.bucket
        self.wrapper = Wrapper()
        self.api.start()
