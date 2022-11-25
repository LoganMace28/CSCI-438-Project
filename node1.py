import socket
import threading

#create main function
def main():
    s = socket.socket()

    port = 100001

    nodeInfo = {"1", "u-02.sm201.iuk.edu",port, "2", "3", "1000"} 

    portInfo = {"1": 100001, "2": 100002, "3": 100003, "4": 100004}

    s.bind(('', port))
    print ("socket bound to %s" %(port))



    while True:
        threading.Thread(target=listening, args=s).start()
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

def listening (s):
    #Listen for incoming connections
    s.listen(5)
    print ("socket is listening")
    return True

main()