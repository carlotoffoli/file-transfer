from socket import *
from threading import Thread
from time import sleep

LOCALIP = '0.0.0.0'

class Controller():
    """
    TCP data transmission with UDP device advertising
    """

    broadcaster = socket()
    broadcaster = socket()
    PORT_SERVER = 5000
    PORT_BROADCAST = 5555
    MSG = bytes(gethostname()+str(PORT_SERVER), 'utf-8')
    MAX_CONNECTIONS = 5
    BEACON = 1
    
    def __init__(self) -> None:
        pass

    def Send(self):
        """
        Select target(s) from available ones, send file to them
        """

    def Receive(self):
        """
        Send broadcast message and receive file
        """

        # Close any open socket
        self.broadcaster.close()

        # Setup UDP broadcasting
        self.broadcaster = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.broadcaster.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # IP address binding
        self.broadcaster.bind((LOCALIP, self.PORT))

        # Advertising
        self.broadcaster.sendto(self.MSG, ('255.255.255.255', self.PORT))
        sleep(self.BEACON)

    def Connect(self, endpoint_ip, endpoint_port):
        """
        Used to setup the TCP connection before sending infos
        """
        
        # Close any open socket on that port
        self.server.close()

        # TCP socket initialization
        self.server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

        # Endpoint connection
        self.server.connect((endpoint_ip, endpoint_port))