from RTPSocketManager import RTPSocketManager
from RTPSocket import RTPSocket
from RTPPacket import RTPPacket

rtpSocketManager = RTPSocketManager()
rtpSocketManager.bindClient()
socketOne = rtpSocketManager.createSocket()
socketTwo = rtpSocketManager.createSocket()

packetToSend = RTPPacket("127.0.0.1", socketOne.portNumber, 99999, 0, 0, "Hello World!!")
socketOne.sendPacket(packetToSend)

#rtpClientMethods.printPortsAvailable()




