from socket import *
import sys, select, pickle



class RTPPacket:

    def __init__(self, destIP="", srcPort=0, destPort=0, seqNum=0, ackNum=0, dataToSend="", fileReceived=""): #, windowSize, checkSum, type, padding):
        if fileReceived is "":
            self.destIP = destIP
            self.srcPort = srcPort
            self.destPort = destPort
            self.seqNum = seqNum
            self.ackNum = ackNum
            self.data = dataToSend
        else:
            "Should construct packet variable from bit stream version"
            packetReceived = pickle.loads(fileReceived)
            self.destIP = packetReceived.destIP
            self.srcPort = packetReceived.srcPort
            self.destPort = packetReceived.destPort
            self.seqNum = packetReceived.seqNum
            self.ackNum = packetReceived.ackNum
            self.data = packetReceived.data

    def getFileToSend(self):
        "Should return bit stream version of all attributes"
        return pickle.dumps(self)