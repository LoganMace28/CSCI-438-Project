import socket

#create main function
def main():
    
    s = socket.socket()

    port = 123456789

    s.bind(('', port))
    print ("socket bound to %s" %(port))

    s.listen(5)
    print ("socket is listening")

    while True:
        c, addr = s.accept()
        print ('Got connection from', addr)
        c.send('Thank you for connecting')
        c.close()
        break
