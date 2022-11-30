import socket
import threading
import time
import graph


#create main function
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10001

nodeInfo = {"1", "u-02.sm201.iuk.edu", port, "2", "3", "1000"}

portInfo = {"1": 10001, "2": 10002, "3": 10003, "4": 10004}

myGraph = graph.Graph(4)
inputGraph = [[0, 1000, 1000, 0],
             [1200, 0, 0, 1200],
             [600, 0, 0, 600],
             [0, 800, 800, 0]]
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
			sendAck(message)
			time.sleep(1)
			if message[1] == "1":
				print(message[2])
			else:
				forward(message)
		break

def send():
	while True:
		print("To send a message, input which node you want to send to: ")
		receivingNode = input()
		print("Thanks, now enter your message: ")
		message = "1|" + receivingNode + "|" + input()
		s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
		x = 0
		while receiveAck() and x < 5:
			x+=1
			print("Ack not received, trying again")
			s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))



def sendAck(c):
		s.sendto("1| Ack".encode(), ('127.0.0.1', portInfo[c[0]]))

def receiveAck():
	s.settimeout(1)
	c, addr = s.recvfrom(1024)
	message = c.decode()
	message = message.split("|")
	if (message[1] == "Ack"):
		print("Received ack")
		return False
	else: 
		return True

def forward(message):
	if message[0] == '2':
		print("Message forwarded to node 2.")
		message = message[0] + '|' + message[1] + '|' + message[2]
		s.sendto(message.encode('ascii'), ('127.0.0.1', portInfo["2"]))
		x = 0
		while receiveAck() and x < 5:
			x+=1
			print("Ack not received, trying again")
			s.sendto(message.encode(), ('127.0.0.1', portInfo[portInfo["2"]]))
	if message[0] == '3':
		print("Message forwarded to node 3.")
		message = message[0] + '|' + message[1] + '|' + message[2]
		s.sendto(message.encode('ascii'), ('127.0.0.1', portInfo["3"]))
		x = 0
		while receiveAck() and x < 5:
			x+=1
			print("Ack not received, trying again")
			s.sendto(message.encode(), ('127.0.0.1', portInfo["3"]))
	

recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()
