import socket


#create main function
def main():
    s = socket.socket()

    port = 100002

    nodeInfo = {"2", "u-02.sm201.iuk.edu",port, "1", "4", "1200"} 

    portInfo = {"1": 100001, "2": 100002, "3": 100003, "4": 100004}

    s.bind(('', port))
    print ("socket bound to %s" %(port))
    
    s.listen(5)
    print ("socket is listening")

    while True:
        s.connect(('127.0.0.1', portInfo["1"]))
        print (s.recv(1024).decode())
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