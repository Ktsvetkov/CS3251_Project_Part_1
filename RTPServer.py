from RTPSocketManager import RTPSocketManager
from RTPSocket import RTPSocket
from RTPPacket import RTPPacket
import time

class RTPServer:

    @staticmethod
    def receiveData(socketToReceiveFileAt):
        dataArray = []

        #listen()
        while 1:
            packetReceived = socketToReceiveFileAt.recvPacket()
            if packetReceived.packetType == "connect":
                break

        #accept()
        packetToSend = RTPPacket("127.0.0.1", packetReceived.srcPort, socketToReceiveFileAt.portNumber, "accept", 0, 1, "")
        socketToReceiveFileAt.sendPacket(packetToSend)

        #dataTransfer()
        while 1:
            try:
                packetReceived = socketToReceiveFileAt.recvPacket()
                if packetReceived.packetType == "data":
                    dataArray.append(packetReceived.data)
                packetTypeToSend = "data"
                if packetReceived.packetType == "close":
                    packetTypeToSend = "close"
                packetToSend = RTPPacket("127.0.0.1", packetReceived.srcPort, socketToReceiveFileAt.portNumber, packetTypeToSend, packetReceived.seqNum, packetReceived.ackNum + 1, "")
                socketToReceiveFileAt.sendPacket(packetToSend)
                if packetReceived.packetType == "close":
                    break
            except Exception as e:
                break

        print "\nConnection Closed\n"

        return dataArray

    @staticmethod
    def writeDataArrayToFile(dataArray):
        fileName = str(int(round(time.time() * 1000)))
        fileReceived = open(fileName + '.jpg', 'wb+')
        for data in dataArray:
            fileReceived.write(data)
        fileReceived.close()






