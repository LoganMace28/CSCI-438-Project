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
		print(c)
def send():
	while True:
		print("To send a message, input which node you want to send to: ")
		receivingNode = input()
		print("Thanks, now enter your message: ")
		message = "From node 4: " + input()
		s.sendto(message.encode('ascii'), ('127.0.0.1', portInfo[receivingNode]))

recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()
