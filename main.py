from socket import *
from threading import Thread
from time import sleep, time

scanning = True
broadcasting = True

THIS = bytes(gethostname(), 'utf-8')

PORT = 5005
BEACON = 2
TIMEOUT = 5
AUTOACCEPT = False

devices = {}

"""
Structure of devices list:

{
    '1.1.1.1': {
        'hostname': 'pc0',
        'port': 5005,
        'last_beacon': 1682422153        
    }
}

"""

def broadcast():
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.bind(('192.168.178.27', PORT))

    while broadcasting:
        s.sendto(THIS, ('255.255.255.255', PORT))
        sleep(BEACON)
    
    s.close()

def scan():
    global devices, scanning

    scanning = True

    Thread(target=scanManager).start()

    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    s.setblocking(False)
    s.bind(('192.168.178.27', PORT))
    
    while scanning:
        try:
            name, endpoint = s.recvfrom(256)
            devices[endpoint[0]] = {
                'hostname': str(name, 'utf-8'),
                'port': endpoint[1],
                'last_beacon': time()
            }
        except error:
            sleep(0.1)
            
    s.close()

def scanManager():
    global devices

    while scanning:
        for ip, info in devices.items():
            if (info['last_beacon'] + TIMEOUT) < time():
                devices.pop(ip)
        sleep(TIMEOUT)

if __name__ == '__main__':
    scanThread = Thread(target=scan)
    scanThread.start()

    for _ in range(10):
        print(devices)
        sleep(BEACON)

    print("Scan terminated... stopping")

    scanning = False