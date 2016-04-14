from RTPSocket import RTPSocket
from socket import *
import sys, select


class RTPSocketManager:

    def __init__(self):
        self.portsAvailable = []
        self.portsTaken = []
        portAssigner = 0
        while len(self.portsAvailable) < 100000:
            self.portsAvailable.append(portAssigner)
            portAssigner += 1
        print 'RTPSocketManager created'
        self.mainSocket = socket(AF_INET, SOCK_DGRAM)

    def bindServer(self):
        self.mainSocket.bind(('', 8591))

    def bindClient(self):
        self.mainSocket.bind(('', 8592))

    def createSocket(self):
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
        return socketToReturn


    def printPortsAvailable(self):
        for port in self.portsAvailable:
            if port not in self.portsTaken:
                print port
        return
