import socket


class Utils:
    @staticmethod
    def getMyIpAdress():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        myIp = s.getsockname()[0]
        s.close()
        print str(myIp)
        return myIp
