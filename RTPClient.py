from RTPSocketManager import RTPSocketManager
from RTPSocket import RTPSocket
from RTPPacket import RTPPacket


def sendData():
    #socket() and bind()
    rtpSocketManager = RTPSocketManager()
    rtpSocketManager.bindClient()
    socketOne = rtpSocketManager.createSocket()

    #connect()
    packetToSend = RTPPacket("127.0.0.1", 99999, socketOne.portNumber, "connect", 0, 0, "")
    socketOne.sendPacket(packetToSend)

    #dataTransfer()
    while 1:
        packetReceived = socketOne.recvPacket()
        packetTypeToSend = "data"
        if packetReceived.seqNum >= 10:
            packetTypeToSend = "close"
        packetToSend = RTPPacket("127.0.0.1", 99999, socketOne.portNumber, packetTypeToSend, packetReceived.seqNum + 1, packetReceived.ackNum, "")
        socketOne.sendPacket(packetToSend)
        if packetReceived.packetType == "close":
            break

    print "\nConnection Closed\n"

    return




sendData()



