from socket import *

s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

s.bind(('192.168.178.27', 5005))

while 1:
    m = s.recvfrom(1024)
    print(m)