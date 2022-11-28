import socket
import threading
import graph


#create main function
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10004

nodeInfo = {"1", "u-02.sm201.iuk.edu", port, "2", "3", "800"}

portInfo = {"1": 10001, "2": 10002, "3": 10003, "4": 10004}

myGraph = graph.Graph(4)
inputGraph = [[0, 800, 800, 0],
             [1200, 0, 0, 1200],
             [600, 0, 0, 600],
             [0, 1000, 1000, 0]]
myGraph.graph = inputGraph
print("Here is the shortest distance to each node")
myGraph.dijkstra(0)

s.bind(('', port))
print ("socket bound to %s" %(port))

def receive():
	while True:
		c, addr = s.recvfrom(1024)
		message = c.split("|")
		mes = str(c)
		message = mes.split("|")
		print(message[1])
		RackThread = threading.Thread(target=sendAck, args=(message,))
		RackThread.start()
def send():
	while True:
		print("To send a message, input which node you want to send to: ")
		receivingNode = input()
		print("Thanks, now enter your message: ")
		message = "4| " + input()
		s.sendto(message.encode('ascii'), ('127.0.0.1', portInfo[receivingNode]))
		SackThread = threading.Thread(target=receiveAck)
		SackThread.start()
def sendAck(c):
		s.sendto("4| Ack".encode('ascii'), ('127.0.0.1',portInfo[c[0]]))

def receiveAck():
	while True:
		c, addr = s.recvfrom(1024)
		message = c.split("|")
		if (message[1] == "Ack"):
			print("Received ack")
		else: 
			print("no ack received")

recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()
