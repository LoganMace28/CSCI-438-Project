import socket
import threading
import time


# make socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# This is the port number for node 1
port = 10001

# Node info for node 1
nodeInfo = {"1", "u-02.sm201.iuk.edu", port, "2", "3", "1000"}

# Port info for node 1
portInfo = {"1": 10001, "2": 10002, "3": 10003, "4": 10002}

# Bind socket s to the port number
s.bind(('', port))
print ("socket bound to %s" % (port))

# Receive method, constantly being ran.
def receive():
    while True:
        # This is responsible for receiving any messages that come through
        c, addr = s.recvfrom(1024)
        message = c.decode()
        message = message.split("|")
        # If the message is not an ACK then this will be true, else we get sent to the
        # receiveAck method
        if message[3] != "Ack":
            sender = message[0]
            # If message was meant for 1, then go to sendAck method, with sender as a parameter
            # then print the message.
            if message[1] == "1":
                sendAck(sender)
                print("-> " + message[3] +  " [" + message[0] + "]")
            else:
                # If the message was not meant for 1, then we create a thread to go to the forward method.
                fowardThread = threading.Thread(target=forward, args=(message[0], message[1], message[2], message[3]))
                fowardThread.start()
        else:
            receiveAck()

# Send method, constantly being ran.
def send():
    while True:
        global x, received, length, forwarded
        # This asks the user where they want to send the message.
        print("To send a message, input which node you want to send to (1-4): ")
        receivingNode = input()
        # If it is not 1-4, then that is a problem so we alert the user then ask again.
        if not (receivingNode == "1" or receivingNode == "2" or receivingNode == "3" or receivingNode == "4"):
            print("Use a number 1-4 please.")
            continue
        # Here is where we ask for the message.
        print("Thanks, now enter your message: ")
        # Set ttl
        ttl =str(1)
        # Concatenate the message, so we send a string and not an array.
        message = "1|" + receivingNode + "|" + ttl + "|" + input()
        # This send the message to the associated port number.
        s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
        # Set forwarded too false to display that the ACK must be displayed here as a check
        forwarded = False
        x = 1
        length = str(len(message))
        # Wait
        time.sleep(2)
        # This while loop is responsible for resending the message in the case that the ACK was not received.
        while received and x < 6:
            x += 1
            message = message.split("|")
            message[2] = str(int(message[2]) + 1)
            message = message[0] + '|' + message[1] + '|' + message[2] + '|' + message[3]
            print("Ack not received, increasing ttl and trying again...")
            s.sendto(message.encode(), ('127.0.0.1', portInfo[receivingNode]))
            time.sleep(2)
            # This if statement displays the x if the message never went through
            if x == 6:
                print("Ack not received, message failed to send.")
                print("\033["+ "7" +"A", end="")
                print("\033[" + length + "C", end="")
                print(u'\u2717', end="\n\n\n\n\n\n\n")
        # Remake receive true in the case it got sent to false, in preparation for the next send.
        received = True

# sendAck method
def sendAck(c):
    global forwarded
    # If forwarded send the ACK to the original sender, else send it where it came from.
    if forwarded == True:
        s.sendto("1|-1|-1|Ack".encode(), ('127.0.0.1', portInfo[c[3]]))
        print ("Ack sent to " + c[3])
    else:
        s.sendto("1|-1|-1|Ack".encode(), ('127.0.0.1', portInfo[c[0]]))


# receiveAck method
def receiveAck():
    global received, forwarded
    # Make received false so the message does not resend, then, as long as the message wasn't
    # forwarded display the check mark.
    received = False
    if forwarded == False:
        print("\033["+ str(x) + "A", end="")
        print("\033[" + str(length) + "C", end="")
        print(u'\u2713')

# forward method, will have its own thread run this on occasion, then the thread dies.
# Associated thread declared in line 40 in method receive.
def forward(message0, message1, message2, message3):
    global received, x, length, forwarded
    message2 = int(message2) - 1
    # Display that ttl expired, or if it didn't then forward the message on to either 2 or 3
    # depending on what the message declares.
    if message2 < 1:
        print("Message ttl expired")
    else:
        message2 = str(message2)
        forwarded = True
        x = 1
        message0 ='1<-' + message0 
        if message1 == '2':
            announcement = "Message forwarded to node 2" 
            print(announcement)
            length = len(announcement)
            # concatenate the message, send it on, then wait a second.
            message = message0 + '|' + message1 + '|' + message2 + '|' + message3
            s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
            time.sleep(1)

        if message1 == '3':
            print("Message forwarded to node 3.")
            # concatenate the message, send it on, then wait a second.
            message = message0 + '|' + message1 + '|' + message2 + '|' + message3
            s.sendto(message.encode(), ('127.0.0.1', portInfo[message1]))
            time.sleep(1)
        # Either send the ACK if message went through or display it failed.
        if received == False:
            sendAck(message)
        else:
            print("Message forward failed.")
        # Turn recieved back to false in case it was changed to true, then wait a second for the
        # message to pass through, then change forwarded back to false.
        received = True
        time.sleep(1)
        forwarded = False    	





# Declare all the global variables.
global forwarded, received, x, length
x = 1
forwarded = False
length = 0
received = True
# here is where the two main thread start for the recieve method and the send method.
recieveThread = threading.Thread(target=receive)
recieveThread.start()
sendThread = threading.Thread(target=send)
sendThread.start()