from RTPSocket import RTPSocket
from RTPSocketManager import RTPSocketManager
from RTPPacket import RTPPacket
import sys, select, socket
import threading


def getDataArrayToSend(fileToSend):
    dataArray = []
    while 1:
        chunk = fileToSend.read(128) #128 bit chunks
        dataArray.append(chunk)
        if not chunk:
            break
    return dataArray

def checkForDownloadedDataThread():
    threading.Thread(target=checkForDownloadedData).start()
    print "\nCreated Thread for Checking for Downloads"

def checkForDownloadedData():
    while 1:
        for socketUsed in socketManager.sockets:
            if socketUsed.hasData == 1:
                fileToReceive = open(fileName, 'wb+')
                for dataChunk in socketUsed.dataReceived:
                    fileToReceive.write(dataChunk)
                fileToReceive.flush()
                fileToReceive.close()
                socketUsed.dataReceived = []
                socketUsed.hasData = 0

########################################
# CHECK PARAMETERS & make socketManager
########################################

ipAddress = ""
udpPort = -1
maxWindowSize = -1

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


fileName = "get_"

#thread to check for file download
checkForDownloadedDataThread()

askForInput = 0

while 1:
    if askForInput == 0:
        askForInput = 1
        action = raw_input("\nPlease enter command: \n")
        actionArray = action.split(" ")
        if actionArray[0] == "disconnect":
            break
        elif actionArray[0] == "get":
            fileName = fileName + actionArray[1]
            socket.sendData("get", ipAddress, 99999, [actionArray[1]])
        elif actionArray[0] == "get-post":
            print "Not yet supported"
            askForInput = 0




