from random import randint

from server.Model.Statut import statut


class Utilisateur:
    def __init__(self, sock):
        self.ip = ""
        self.numTel = self.generatePhoneNumber()
        self.sock = sock
        self.statut = statut.READY_FOR_CONVERSATION

    def generatePhoneNumber(self):
        return "06"+str(randint(10000000,99999999))

