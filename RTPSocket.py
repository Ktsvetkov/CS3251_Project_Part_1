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
        portToSendTo = 8591
        if self.mainSocket.getsockname()[1] == 8591:
            portToSendTo = 8592
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



"""#Check arguments length is valid
if len(sys.argv) < 4:
    print "Please use valid number of arguments"
    sys.exit()

#Parse paramteres
try:
    params = ""
    i = 0
    for arg in sys.argv:
        i = i + 1
        if i == 2:
            addressArray = arg.split(":")
            if len(addressArray) < 2:
                print "Please use valid address arguments"
                sys.exit()
            serverIpAddress = addressArray[0]
            serverPortNumber = int(addressArray[1])
        if i == 3:
            GTID = str(arg)
        if i == 4:
            params = str(arg)
        if i > 4:
            params = params + ", " + str(arg)
except Exception as e:
    print "Failure parsing parameters: " + str(e)
    sys.exit()

#socket()
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setblocking(0)

#try send() and recv() every 2 seconds
modifiedMessage = ""
j = 0;
while modifiedMessage is "" and j < 3:
    j = j + 1
    serverQuery = GTID + ":" + params
    clientSocket.sendto(serverQuery,(serverIpAddress, serverPortNumber))
    ready = select.select([clientSocket], [], [], 2)
    if ready[0]:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    else:
        print "The server has not answered in the last two seconds.\nretrying..."

#print out result
if modifiedMessage is "":
    print "Error no response from engine after 3 attempts"
else:
    print 'From Server:', modifiedMessage

#close()
clientSocket.close()"""

