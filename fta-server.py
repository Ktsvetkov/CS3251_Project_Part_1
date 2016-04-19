from RTPSocket import RTPSocket
from RTPSocketManager import RTPSocketManager
from RTPPacket import RTPPacket
import sys, select, socket
import threading
import time

def getDataArrayToSend(fileToSend):
    dataArray = []
    while 1:
        chunk = fileToSend.read(128) #128 bit chunks
        dataArray.append(chunk)
        if not chunk:
            break
    return dataArray

def checkForDownloadedDataThread():
    checkForDataThread = threading.Thread(target=checkForDownloadedData)
    checkForDataThread.daemon = True
    checkForDataThread.start()
    print "\nCreated Thread for Checking for Downloads"

def checkForDownloadedData():
    while 1:
        for socketUsed in socketManager.sockets:
            if socketUsed.hasData == 1:
                fileToReceive = open("post_" + socketUsed.dataReceivedName, 'wb+')
                for dataChunk in socketUsed.dataReceived:
                    fileToReceive.write(dataChunk)
                fileToReceive.flush()
                fileToReceive.close()
                socketUsed.dataReceived = []
                socketUsed.hasData = 0
                socketUsed.packetReceivedName = ""
        time.sleep(1)


########################################
# CHECK PARAMETERS & make socketManager
########################################

udpPort = -1
maxWindowSize = -1

try:
    if len(sys.argv) != 3:
        print "Please specify a UDP Port and a Maximum Receive Window"
        sys.exit()

    i = 0
    for arg in sys.argv:
        if i == 1:
            udpPort = int(arg)
        if i == 2:
            maxWindowSize = int(arg)
        i = i + 1

    if udpPort == -1 or maxWindowSize == -1:
        print "Invalid Paramteres"
        sys.exit()
except e:
    print "Invalid Paramteres Exception: \n" + str(e.value)
    sys.exit()

########################################

socketManager = RTPSocketManager()
socketManager.bindUDP(str(socket.gethostbyname(socket.getfqdn())), udpPort)
socket = socketManager.createSocket()


#thread to check for file download
checkForDownloadedDataThread()

while 1:
    for socketUsed in socketManager.sockets:
        if socketUsed.readyForGet == 1:
            print "Detected a socket ready for a request"
            fileToSend = open(socketUsed.fileToGet, 'rb+')
            dataArray = getDataArrayToSend(fileToSend)
            socketUsed.sendData("post", socketUsed.outgoingConnectionIP, socketUsed.outgoingConnectionPort, dataArray, socketUsed.fileToGet)
    time.sleep(1)


