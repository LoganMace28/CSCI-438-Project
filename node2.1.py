import socket
import threading
import graph
import time


# create main functions
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
		if message[2] != "Ack":
			sendAck(message)
			if message[1] == "2":
				print(message[2])
			else:
				forward(message)
		else:
			receiveAck(message)

def send():
	while True:
		print("To send a message, input which node you want to send to (1-4): ")
		receivingNode = input()
		if not (receivingNode == "1" or receivingNode == "2" or receivingNode == "3" or receivingNode == "4"):
			print("Use a number 1-4 please.")
			continue
		print("Thanks, now enter your message: ")
		message = "2|" + receivingNode + "|" + input()
		s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
		x = 0
		global received
		time.sleep(2)
		while received and x < 5:
			x+=1
			print("Ack not received, trying again")
			s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
			time.sleep(2)
		received = True

def sendAck(c):
	s.sendto("2|-1|Ack".encode(), ('127.0.0.1', portInfo[c[0]]))

def receiveAck(message):
	global received
	received = False
	print("Received ack")

def forward(message):
	global received
	x = 0
	if message[0] == '1':
		print("Message forwarded to node 1.")
		message = message[0] + '|' + message[1] + '|' + message[2]
		s.sendto(message.encode('ascii'), ('127.0.0.1', portInfo["1"]))
		time.sleep(2)
		while received and x < 5:
			x+=1
			print("Ack not received, trying again")
			s.sendto(message.encode(), ('127.0.0.1', portInfo[portInfo["1"]]))
			time.sleep(2)
	if message[0] == '4':
		print("Message forwarded to node 4.")
		message = message[0] + '|' + message[1] + '|' + message[2]
		s.sendto(message.encode('ascii'), ('127.0.0.1', portInfo["4"]))
		time.sleep(2)
		while received and x < 5:
			x+=1
			print("Ack not received, trying again")
			s.sendto(message.encode(), ('127.0.0.1', portInfo["4"]))
			time.sleep(2)
		received = True

received = True
recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()