import socket
import time
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# here we asking for the target website
# or host
target = "localhost"

# I think this will be our ITC script and the nodes will pull info from it 
nodeInfo = {{"1", "u-02.sm201.iuk.edu",10001, "2", "3", "1000"},
            {"2", "u-02.sm201.iuk.edu",10002, "1", "4", "1200"},
            {"3", "u-07.sm201.iuk.edu",10003, "1", "4", "600"},
            {"4", "u-12.sm201.iuk.edu",10004, "2", "3", "800"}}

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