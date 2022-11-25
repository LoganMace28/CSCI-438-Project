import socket
import time
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# here we asking for the target website
# or host
target = "localhost"
 
# next line gives us the ip address
# of the target
target_ip = socket.gethostbyname(target)
print('Starting scan on host:', target_ip)
 
# function for scanning ports
 
 
def port_scan(port):
    try:
        s.connect((target_ip, port))
        return True
    except:
        return False
 
 
start = time.time()
 
# here we are scanning port 0 to 4
for port in range(10001, 10005):
    if port_scan(port):
        print(f'port {port} is open')
    else:
        print(f'port {port} is closed')
 
end = time.time()
print(f'Time taken {end-start:.2f} seconds')