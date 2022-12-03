import socket
import threading
import graph
import time


# create main functions
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10002

nodeInfo = {"2", "u-02.sm201.iuk.edu", port, "1", "4", "1200"}

portInfo = {"1": 10001, "2": 10002, "3": 10001, "4": 10004}

myGraph = graph.Graph(4)
inputGraph = [[0, 1200, 0, 1200],
             [1000, 0, 1000, 0],
             [0, 600, 0, 600],
             [800, 0, 800, 0]]
myGraph.graph = inputGraph
print("Here is the shortest distance to each node")
myGraph.dijkstra(0)

s.bind(('', port))
print ("socket bound to %s" %(port))

def receive():
    while True:
        c, addr = s.recvfrom(1024)
        message = c.decode()
        message = message.split("|")
        if message[2] != "Ack":
            sender = message[0]
            if message[1] == "2":
                sendAck(sender)
                print("-> " + message[2] +  " [" + message[0] + "]")
            else:
                fowardThread = threading.Thread(target=forward, args=(message[0], message[1], message[2]))
                fowardThread.start()
        else:
            receiveAck()

def send():
    while True:
        global x, received, length, forwarded
        print("To send a message, input which node you want to send to (1-4): ")
        receivingNode = input()
        if not (receivingNode == "1" or receivingNode == "2" or receivingNode == "3" or receivingNode == "4"):
            print("Use a number 1-4 please.")
            continue
        print("Thanks, now enter your message: ")
        message = "2|" + receivingNode + "|" + input()
        s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
        forwarded = False
        x = 1
        length = str(len(message))
        time.sleep(2)
        while received and x < 6:
            x += 1
            print("Ack not received, trying again...")
            s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
            time.sleep(2)
            if x == 6:
                print("Ack not received, message failed to send.")
                print("\033["+ "7" +"A", end="")
                print("\033[" + length + "C", end="")
                print(u'\u2717', end="\n\n\n\n\n\n\n")
                
        received = True
def sendAck(c):
	s.sendto("2|-1|Ack".encode(), ('127.0.0.1', portInfo[c[0]]))

def receiveAck():
	global received
	received = False
	if forwarded == False:
		print("\033["+ str(x) + "A", end="")
		print("\033[" + length + "C", end="")
		print(u'\u2713')

def forward(message0, message1, message2):
    global received, x, length, forwarded
    forwarded = True
    length = str(len(message2))
    x = 1
    message0 = '2<-' + message0
    if message1 == '1':
        print("Message forwarded to node 1.")
        message = message0 + '|' + message1 + '|' + message2
        s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
        time.sleep(1)
        while received and x < 6:
            x += 1
            print("Ack not received, trying again")
            s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
            time.sleep(1)
        if received == False:
            sendAck(message)
    if message1 == '4':
        print("Message forwarded to node 4.")
        message = message0 + '|' + message1 + '|' + message2
        s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
        time.sleep(1)
        while received and x < 5:
            x += 1
            print("Ack not received, trying again")
            s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
            time.sleep(1)
        if received == False:
            sendAck(message)
    forwarded = False
    received = True


forwarded = False
received = True
recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()