# coding=utf-8
from server.Model.Command import command


class Bucket:
    def __init__(self):
        self.messages = []

    def addMessage(self,message):
        print "Message reçu: " + message
        self.messages.append(message)

    def getLastMessage(self):
        size=self.messages.__len__()
        return self.messages[size - 1] if size > 0 else "/n "

    def getInnerMessage(self):
        return self.getLastMessage()[3:]

    def getNatureOfLastMessage(self):
        cmd = self.getLastMessage().__getitem__(1)
        vretour = command.NULL
        if cmd == command.ERROR :
           vretour = command.ERROR
        elif cmd ==  command.INFO:
            vretour = command.INFO
        elif cmd == command.MESSAGE:
            vretour = command.MESSAGE
        elif cmd == command.STATUS:
            vretour = command.STATUS
        elif cmd == command.ASK:
            vretour = command.ASK
        return vretour