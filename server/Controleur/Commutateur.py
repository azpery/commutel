# coding=utf-8
import socket
import select
from threading import Thread
from server.Controleur.ActionHandler import ActionHandler
from server.Infra.Config import config
from server.Model.Utilisateur import Utilisateur


class Commutateur:
    def __init__(self):
        self.actionHandler = ActionHandler(self)
        self.connectedUser = []
        self.CONNECTION_LIST = []
        self.RECV_BUFFER = config["RECV_BUFFER"]
        self.PORT = config["PORT"]

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", self.PORT))
        self.server_socket.listen(10)

        self.CONNECTION_LIST.append(self.server_socket)

        print "Chat server started on port " + str(self.PORT)

        self.threadListenner = Thread(target=self.mainLoop())
        self.threadListenner.start()

    def mainLoop(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])

            for sock in read_sockets:

                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.CONNECTION_LIST.append(sockfd)
                    utilisateur = Utilisateur(sockfd)
                    self.connectedUser.append(utilisateur)
                    print "Client (%s, %s) connected" % addr
                    self.actionHandler.initiateConnectionWithNewUser(utilisateur)
                else:
                    try:
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            print data
                            self.actionHandler.handle(data, sock)

                    except:
                        #self.sendMessageTo(sock, "Client (%s, %s) if offline" % addr)
                        sock.close()
                        self.CONNECTION_LIST.remove(sock)
                        continue

        self.server_socket.close()

    def sendMessageTo(self, socket, message):
        print "Envoie de message : "+message
        if socket != self.server_socket:
            try:
                socket.send(message)
            except:
                socket.close()
                self.CONNECTION_LIST.remove(socket)