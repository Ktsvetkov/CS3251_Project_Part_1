from RTPSocketManager import RTPSocketManager
from RTPSocket import RTPSocket
from RTPPacket import RTPPacket


def receiveData():
    #socket() and bind()
    rtpSocketManager = RTPSocketManager()
    rtpSocketManager.bindServer()
    socketOne = rtpSocketManager.createSocket()

    #listen()
    while 1:
        packetReceived = socketOne.recvPacket()
        if packetReceived.packetType == "connect":
            break

    #accept()
    packetToSend = RTPPacket("127.0.0.1", 99999, socketOne.portNumber, "accept", 0, 1, "")
    socketOne.sendPacket(packetToSend)

    #dataTransfer()
    while 1:
        packetReceived = socketOne.recvPacket()
        packetTypeToSend = "data"
        if packetReceived.seqNum >= 10:
            packetTypeToSend = "close"
        packetToSend = RTPPacket("127.0.0.1", 99999, socketOne.portNumber, packetTypeToSend, packetReceived.seqNum, packetReceived.ackNum + 1, "")
        socketOne.sendPacket(packetToSend)
        if packetReceived.packetType == "close":
            break

    print "\nConnection Closed\n"

    return



receiveData()


