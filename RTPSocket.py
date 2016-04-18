from RTPPacket import RTPPacket
from socket import *
import sys, select




class RTPSocket:

    def __init__(self, portNumber, mainSocket):
        self.portNumber = portNumber
        self.mainSocket = mainSocket

    def getPortNumber(self):
        return self.portNumber

    def connect(self):
       "Send packet with data bits for connect"
       return

    def sendPacket(self, packetToSend):
        "sends RTPPacket to where it should go"
        print "Sent Packet Called"
        portToSendTo = 8591
        if self.mainSocket.getsockname()[1] == 8591:
            portToSendTo = 8592
        print "\nPacket Sent to port " + str(packetToSend.destPort) + "\n\tType: " + packetToSend.packetType + "\n\tSequence Number: " + str(packetToSend.seqNum) + "\n\tACK Number: " + str(packetToSend.ackNum) + "\n\tMessage: " + packetToSend.data
        self.mainSocket.sendto(packetToSend.getFileToSend(),(packetToSend.destIP, portToSendTo))
        return

    def recvPacket(self):
        "return packet deciphered from data bits"
        while 1:
            message, clientAddress = self.mainSocket.recvfrom(2048)
            packetReceived = RTPPacket("", 0, 0, "", 0, 0, "", message)
            if packetReceived.destPort == self.portNumber:
                print "\nPacket Received at port " + str(packetReceived.destPort) + "\n\tType: " + packetReceived.packetType + "\n\tSequence Number: " + str(packetReceived.seqNum) + "\n\tACK Number: " + str(packetReceived.ackNum) + "\n\tMessage: " + packetReceived.data
                return packetReceived

