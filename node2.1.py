import socket
import threading
import graph
import time

#create main function
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10002

nodeInfo = {"2", "u-02.sm201.iuk.edu", port, "1", "4", "1200"}

portInfo = {"1": 10001, "2": 10002, "3": 10003, "4": 10004}

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
		if (message[1] != "Ack"):
			print(message[1])
			sendAck(message)
			time.sleep(1)
		
		

def send():
	while True:
		print("To send a message, input which node you want to send to: ")
		receivingNode = input()
		print("Thanks, now enter your message: ")
		message = "2| " + input()
		s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
		x = 0
		while receiveAck() and x < 5:
			x+=1
			print("Ack not received, trying again")
			s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))

def sendAck(c):
		s.sendto("2|Ack".encode(), ('127.0.0.1',portInfo[c[0]]))
		print("Ack sent")

def receiveAck():
	c, addr = s.recvfrom(1024)
	message = c.decode()
	message = message.split("|")
	if (message[1] == "Ack"):
		print("Received ack")
		return False
	else: 
		return True
		
recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()
