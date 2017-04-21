# coding=utf-8
import select
from threading import Thread
from server.Infra.Config import config
from server.Model.Bucket import Bucket
from server.Model.Command import command
from server.Model.Statut import statut


class CtrlConversation:
    def __init__(self, appelant, appele, parent):
        self.appelant = appelant
        self.appele = appele
        self.appelant.statut = statut.BUSY
        self.appele.statut = statut.BUSY
        self.bucket = Bucket()
        self.CONNECTION_LIST = [appele.sock, appelant.sock]
        self.parent = parent
        self.parent.CONNECTION_LIST.remove(appelant.sock)
        self.parent.CONNECTION_LIST.remove(appele.sock)
        self.RECV_BUFFER = config["RECV_BUFFER"]
        self.stop = False

    def startLoop(self):
        thread1 = Thread(target=self.loop)
        thread1.start()

    def loop(self):
        self.parent.sendMessageTo(self.appele.sock, "/a "+self.appelant.numTel)
        while not self.stop:
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])

            for sock in read_sockets:

                if sock != self.parent.server_socket:
                    try:
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            print "Message dans le salon privé:" + data
                            self.bucket.addMessage(data)
                            if self.bucket.getNatureOfLastMessage() == command.MESSAGE or (self.bucket.getNatureOfLastMessage() == command.STATUS and int(self.bucket.getInnerMessage()) == statut.READY_FOR_CONVERSATION):
                                if self.appele.sock == sock:
                                    self.parent.sendMessageTo(self.appelant.sock, data)
                                else:
                                    self.parent.sendMessageTo(self.appele.sock, data)
                            if self.bucket.getNatureOfLastMessage() == command.STATUS and int(self.bucket.getInnerMessage()) == statut.DISCONNECTED:
                                if self.appele.sock == sock:
                                    self.parent.sendMessageTo(self.appelant.sock, data)
                                else:
                                    self.parent.sendMessageTo(self.appele.sock, data)
                                self.CONNECTION_LIST = []
                                self.stop = True
                                self.parent.CONNECTION_LIST.append(self.appelant.sock)
                                self.parent.CONNECTION_LIST.append(self.appele.sock)


                    except:
                        #self.sendMessageTo(sock, "Client (%s, %s) if offline" % addr)
                        sock.close()
                        #self.CONNECTION_LIST.remove(sock)
                        continue

        #self.server_socket.close()
