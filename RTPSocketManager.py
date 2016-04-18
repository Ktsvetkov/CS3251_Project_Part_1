from RTPSocket import RTPSocket
from socket import *
import sys, select


class RTPSocketManager:

    def __init__(self):
        self.portsAvailable = []
        self.portsTaken = []
        self.sockets = []
        portAssigner = 0
        while len(self.portsAvailable) < 100000:
            self.portsAvailable.append(portAssigner)
            portAssigner += 1
        print 'RTPSocketManager created'
        self.mainSocket = socket(AF_INET, SOCK_DGRAM, 0)

    def bindServer(self):
        self.mainSocket.bind(('', 8591))

    def bindClient(self):
        self.mainSocket.bind(('', 8592))

    def createSocket(self, portNumber=-1):
        if portNumber == -1:
            "Creates socket assigning it to vitual port"
            portToAssign = -1
            for port in self.portsAvailable:
                if port not in self.portsTaken:
                    portToAssign = port
            self.portsTaken.append(portToAssign)
            #do something with port number
            socketToReturn = RTPSocket(portToAssign, self.mainSocket)
            if portToAssign == -1:
                print "All 100,000 port numbers taken"
            else:
                print "Created socket with port: ", portToAssign
            self.sockets.append(socketToReturn)
            return socketToReturn
        else:
            if portNumber not in self.portsTaken:
                self.portsTaken.append(portNumber)
                socketToReturn = RTPSocket(portNumber, self.mainSocket)
                self.sockets.append(socketToReturn)
                return socketToReturn
            else:
                print "Socket Already Taken"

    def getSocket(self, portNumber):
        for socket in self.sockets:
            if socket.portNumber == portNumber:
                return socket

    def printPortsAvailable(self):
        for port in self.portsAvailable:
            if port not in self.portsTaken:
                print port
        return

    def getPortsUsed(self):
        return self.portsTaken

    def getPortsUsedString(self):
        portsUsedArray = self.getPortsUsed()
        portsUsedString = ""
        for usedPort in portsUsedArray:
            portsUsedString = portsUsedString + str(usedPort) + ", "
        if portsUsedString == "":
            return portsUsedString
        else:
            return portsUsedString[:-1]

