import time

from server.Controleur.CtrlConversation import CtrlConversation
from server.Model.Bucket import Bucket
from server.Model.Command import command
from server.Model.Statut import statut
from server.Utils.Wrapper import Wrapper


class ActionHandler:

    def __init__(self, parent):
        self.bucket = Bucket()
        self.parent = parent

    def handle(self,data, sock):
        self.bucket.addMessage(data)
        if self.bucket.getNatureOfLastMessage() == command.ASK:
            if self.isDestAvailable(self.bucket.getInnerMessage()):
                appele = self.getUserFromNumTel(self.bucket.getInnerMessage())
                appelant = self.getUserFromSock(sock)
                ctrlCommunication = CtrlConversation(appelant,appele,self.parent)
                ctrlCommunication.startLoop()

    def initiateConnectionWithNewUser(self, user):
        self.parent.sendMessageTo(user.sock, Wrapper.wrapStatus("202"))
        time.sleep(1)
        self.parent.sendMessageTo(user.sock, Wrapper.wrapMessage(user.numTel))

    def isDestAvailable(self, numTel):
        for user in self.parent.connectedUser :
            if user.numTel == numTel and user.statut == statut.READY_FOR_CONVERSATION:
                return True
        return False

    def getUserFromNumTel(self,numTel):
        for user in self.parent.connectedUser :
            if user.numTel == numTel:
                return user

    def getUserFromSock(self,sock):
        for user in self.parent.connectedUser :
            if user.sock == sock:
                return user