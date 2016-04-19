from RTPSocket import RTPSocket
from RTPSocketManager import RTPSocketManager
from RTPPacket import RTPPacket
import sys, select, socket
import threading
import time
from termios import tcflush, TCIFLUSH


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
    global askForInput
    while 1:
        for socketUsed in socketManager.sockets:
            if socketUsed.hasData == 1:
                fileToReceive = open("get_" + socketUsed.dataReceivedName, 'wb+')
                for dataChunk in socketUsed.dataReceived:
                    fileToReceive.write(dataChunk)
                fileToReceive.flush()
                fileToReceive.close()
                socketUsed.dataReceived = []
                socketUsed.hasData = 0
                socketUsed.packetReceivedName = ""
                askForInput = 0
        time.sleep(1)

########################################
# CHECK PARAMETERS & make socketManager
########################################

ipAddress = ""
udpPort = -1
maxWindowSize = -1
fileName = ""
askForInput = 0


try:
    if len(sys.argv) != 3:
        print "Please specify a UDP Port and a Maximum Receive Window"
        sys.exit()

    i = 0
    for arg in sys.argv:
        if i == 1:
            addresses = str(arg).split(':')
            ipAddress = addresses[0]
            udpPort = addresses[1]
        if i == 2:
            maxWindowSize = int(arg)
        i = i + 1

    if udpPort == -1 or maxWindowSize == -1 or ipAddress == "":
        print "Invalid Paramteres"
        sys.exit()
except e:
    print "Invalid Paramteres Exception: \n" + str(e.value)
    sys.exit()

########################################

socketManager = RTPSocketManager()
socketManager.bindUDP(str(socket.gethostbyname(socket.getfqdn())), 8592)
socket = socketManager.createSocket()


#thread to check for file download
checkForDownloadedDataThread()

while 1:
    if askForInput == 0:
        askForInput = 1

        tcflush(sys.stdin, TCIFLUSH)
        action = raw_input("\nPlease enter command: \n")
        actionArray = action.split(" ")
        if actionArray[0] == "disconnect":
            break
        elif actionArray[0] == "get":
            fileName = "get_" + actionArray[1]
            socket.sendData("get", ipAddress, 99999, [actionArray[1]])
        elif actionArray[0] == "get-post":
            fileToSend = open(actionArray[2], 'rb+')
            dataArray = getDataArrayToSend(fileToSend)
            socket.sendData("post", ipAddress, 99999, dataArray, actionArray[2])
            fileName = "get_" + actionArray[1]
            socket.sendData("get", ipAddress, 99999, [actionArray[1]])
    else:
        time.sleep(1)


