import socket
import threading
import time

# Functionally the same as all other nodes, just with node 4 info
# create main functions
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10004

nodeInfo = {"4", "u-02.sm201.iuk.edu", port, "2", "3", "800"}

portInfo = {"1": 10003, "2": 10002, "3": 10003, "4": 10004}

s.bind(('', port))
print ("socket bound to %s" % (port))

def receive():
    while True:
        c, addr = s.recvfrom(1024)
        message = c.decode()
        message = message.split("|")
        if message[3] != "Ack":
            sender = message[0]
            if message[1] == "4":
                sendAck(sender)
                print("-> " + message[3] +  " [" + message[0] + "]")
            else:
                fowardThread = threading.Thread(target=forward, args=(message[0], message[1], message[2], message[3]))
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
        ttl =str(1)
        message = "4|" + receivingNode + "|" + ttl + "|" + input()
        s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
        forwarded = False
        x = 1
        length = str(len(message))
        time.sleep(2)
        while received and x < 6:
            x += 1
            message = message.split("|")
            message[2] = str(int(message[2]) + 1)
            message = message[0] + '|' + message[1] + '|' + message[2] + '|' + message[3]
            print("Ack not received, increasing ttl and trying again...")
            s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
            time.sleep(2)
            if x == 6:
                print("Ack not received, message failed to send.")
                print("\033["+ "7" +"A", end="")
                print("\033[" + length + "C", end="")
                print(u'\u2717', end="\n\n\n\n\n\n\n")
                
        received = True


def sendAck(c):
    global forwarded
    if forwarded == True:
        s.sendto("4|-1|-1|Ack".encode(), ('127.0.0.1', portInfo[c[3]]))
        print ("Ack sent to " + c[3])
    else:
        s.sendto("4|-1|-1|Ack".encode(), ('127.0.0.1', portInfo[c[0]]))
        print ("Ack sent to " + c[0])


def receiveAck():
	global received, forwarded
	received = False
	if forwarded == False:
		print("\033["+ str(x) + "A", end="")
		print("\033[" + str(length) + "C", end="")
		print(u'\u2713')


def forward(message0, message1, message2, message3):
    global received, x, length, forwarded
    message2 = int(message2) - 1
    if message2 < 1:
        print("Message ttl expired")
    else:
        message2 = str(message2)
        forwarded = True
        x = 1
        message0 ='4<-' + message0 
        if message1 == '2':
            announcement = "Message forwarded to node 2" 
            print(announcement)
            length = len(announcement)
            message = message0 + '|' + message1 + '|' + message2 + '|' + message3
            s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
            time.sleep(1)

        if message1 == '3':
            print("Message forwarded to node 3.")
            message = message0 + '|' + message1 + '|' + message2 + '|' + message3
            s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
            time.sleep(1)
        if received == False:
            sendAck(message)
        else:
            print("Message forward failed.")
        received = True
        time.sleep(1)
        forwarded = False    	



global forwarded, received, x, length
x = 1
forwarded = False
length = 0
received = True
recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()
