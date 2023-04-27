from socket import *

s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
# s.setblocking(False)
s.bind(('192.168.178.27', 5005))
print('Starting')
while 1:
    try:
        print("Waiting...")
        m = s.recvfrom(1024)
        print(m)
    except KeyboardInterrupt:
        break

s.close()