from RTPSocketManager import RTPSocketManager
from RTPSocket import RTPSocket
from RTPPacket import RTPPacket
import multiprocessing

class RTPClient:

    @staticmethod
    def receiveDataAsync(socketToUse, dataArray, ipAddress, portNumber):
        pool = multiprocessing.Pool()
        pool.apply_async(foo_pool, args = (socketToUse, ), callback = log_result)

    def receivePacketSync(socketToUse)

    @staticmethod
    def sendData(socketToUse, dataArray, ipAddress, portNumber):

        #connect()
        packetToSend = RTPPacket(ipAddress, portNumber, socketToUse.portNumber, "connect", 0, 0, "")
        socketToUse.sendPacket(packetToSend)

        #dataTransfer()
        while 1:
            try:
                print "RTP Client Sending another packet"
                packetReceived = socketToUse.recvPacket()
                print "RTP Client successfully received packet"
                packetTypeToSend = "data"
                if packetReceived.seqNum >= len(dataArray):
                    packetTypeToSend = "close"
                    packetToSend = RTPPacket(ipAddress, portNumber, socketToUse.portNumber, packetTypeToSend, packetReceived.seqNum + 1, packetReceived.ackNum, "")
                else:
                    packetToSend = RTPPacket(ipAddress, portNumber, socketToUse.portNumber, packetTypeToSend, packetReceived.seqNum + 1, packetReceived.ackNum, dataArray[packetReceived.seqNum])
                socketToUse.sendPacket(packetToSend)
                print "RTP Client successfully sent packet"
                if packetReceived.packetType == "close":
                    break
            except Exception as e:
                break

        print "\nConnection Closed\n"

        return

    @staticmethod
    def getDataArrayToSend(fileToSend):
        dataArray = []
        while 1:
            chunk = fileToSend.read(256) #16 bit chunks
            dataArray.append(chunk)
            if not chunk: break
        return dataArray




