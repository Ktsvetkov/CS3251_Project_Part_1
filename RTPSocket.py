from RTPPacket import RTPPacket
from socket import *
import sys, select, socket




class RTPSocket:

    def __init__(self, portNumber, socketManager):
        self.portNumber = portNumber
        self.socketManager = socketManager
        self.srcIP = "127.0.0.1"#str(socket.gethostbyname(socket.getfqdn()))

        self.hasData = 0
        self.isSending = 0
        self.isReceiving = 0

        self.incomingConnectionIP = ""
        self.incomingConnectionPort = 0
        self.outgoingConnectionIP = ""
        self.outgoingConnectionPort = 0

        self.dataToSend = []
        self.dataReceived = []
        self.windowSize = 1

    def packetReceived(self, packetReceived):

        #Receiving Methods
        if packetReceived.packetType == "connect":
            self.isReceiving = 1
            self.incomingConnectionIP = packetReceived.srcIP
            self.incomingConnectionPort = packetReceived.srcPort
            packetToSend = RTPPacket(packetReceived.srcIP, packetReceived.srcPort, self.srcIP, packetReceived.destPort, "accept", packetReceived.seqNum, packetReceived.ackNum + 1, "")

            self.socketManager.sendPacket(packetToSend)

        elif packetReceived.packetType == "data":
            self.dataReceived.append(packetReceived.data)
            packetToSend = RTPPacket(packetReceived.srcIP, packetReceived.srcPort, self.srcIP, packetReceived.destPort, "ack", packetReceived.seqNum, packetReceived.ackNum + 1, "")

            self.socketManager.sendPacket(packetToSend)

        elif packetReceived.packetType == "closereceiver":
            self.isReceiving = 0
            self.hasData = 1
            self.incomingConnectionIP = ""
            self.incomingConnectionPort = 0
            packetToSend = RTPPacket(packetReceived.srcIP, packetReceived.srcPort, self.srcIP, packetReceived.destPort, "closesender", 0, 0, "")

            self.socketManager.sendPacket(packetToSend)

        #Sender Methods
        elif packetReceived.packetType == "accept":
            dataChunkToSend = self.dataToSend[packetReceived.seqNum]
            packetToSend = RTPPacket(packetReceived.srcIP, packetReceived.srcPort, self.srcIP, packetReceived.destPort, "data", packetReceived.seqNum + 1, packetReceived.ackNum, dataChunkToSend)

            self.socketManager.sendPacket(packetToSend)

        elif packetReceived.packetType == "ack":
            if packetReceived.seqNum < len(self.dataToSend):
                dataChunkToSend = self.dataToSend[packetReceived.seqNum]
                packetToSend = RTPPacket(packetReceived.srcIP, packetReceived.srcPort, self.srcIP, packetReceived.destPort, "data", packetReceived.seqNum + 1, packetReceived.ackNum, dataChunkToSend)
            else:
                packetToSend = RTPPacket(packetReceived.srcIP, packetReceived.srcPort, self.srcIP, packetReceived.destPort, "closereceiver", 0, 0, "")

            self.socketManager.sendPacket(packetToSend)

        elif packetReceived.packetType == "closesender":
            self.isSending = 0
            self.dataToSend = []
            self.outgoingConnectionIP = ""
            self.outgoingConnectionPort = 0


    def sendData(self, dataToSend, destIP, destPort):
        self.isSending = 1
        self.outgoingConnectionIP = destIP
        self.outgoingConnectionPort = destPort
        self.dataToSend = dataToSend
        packetToSend = RTPPacket(destIP, destPort, self.srcIP, self.portNumber, "connect", 0, 0, "")

        self.socketManager.sendPacket(packetToSend)





