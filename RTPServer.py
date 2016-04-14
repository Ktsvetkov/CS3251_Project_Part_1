from RTPSocketManager import RTPSocketManager
from RTPSocket import RTPSocket
from RTPPacket import RTPPacket

rtpSocketManager = RTPSocketManager()
rtpSocketManager.bindServer()
socketOne = rtpSocketManager.createSocket()
socketTwo = rtpSocketManager.createSocket()

packetReceived = socketOne.recvPacket()

print "\nPacket Received at port " + str(packetReceived.destPort) + "\n\tMessage: " + packetReceived.data + "\n\tSequence Number: " + str(packetReceived.seqNum) + "\n\tACK Number: " + str(packetReceived.ackNum)


#rtpClientMethods.printPortsAvailable()


