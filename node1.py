import socket


#create main function
def main():
    s = socket.socket()

    port = 101

    nodeInfo = {"1", "u-02.sm201.iuk.edu",port, "2", "3", "1000"} 

    portInfo = {"1": 101, "2": 102, "3": 103, "4": 104}

    s.bind(('', port))
    print ("socket bound to %s" %(port))

    s.listen(5)
    print ("socket is listening")

    while True:
        c, addr = s.accept()
        print ('Got connection from', addr)
        c.send('Thank you for connecting')
        c.close()
#create update portInfo function
def updateNodeInfo(nodeInfo, portInfo):
    #Update the nodes that current node can connect to 
    return portInfo


def scanPorts(portInfo):
    #Look at all available ports and see if any have changed
    return True

main()