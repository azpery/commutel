import socket
import select
import sys
from threading import Thread

from client.Infra.Config import config
from client.Model.Bucket import Bucket


class Api:
    def __init__(self, callback):

        self.host = config["host"]
        self.port = config["port"]

        self.bucket =  Bucket()
        self.callback = callback

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(1)

        try:
            self.s.connect((self.host, self.port))
        except Exception, e:
            print 'Error with the connection \n' + str(e)

        self.threadListenner = Thread(target=self.loopListenner)
        self.threadListenner.start()

    def loopListenner(self):
        while True:
            socket_list = [self.s]

            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

            for sock in read_sockets:
                pass
            if sock == self.s:
                data = sock.recv(4096)
                if not data:
                    print 'Error with the connection'
                    sys.exit()
                else:
                    self.bucket.addMessage(data)
                    self.callback(data)

    def send(self, msg):
        self.s.send(msg)
