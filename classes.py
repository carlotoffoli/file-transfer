from socket import *
from threading import Thread
from time import sleep

LOCALIP = '0.0.0.0'

class Controller():
    """
    TCP data transmission with UDP device advertising
    """

    link = socket()
    PORT = 5555
    MSG = gethostname()
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
        self.link.close()

        # Setup UDP broadcasting
        self.link = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.link.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # IP address binding
        self.link.bind((LOCALIP, self.PORT))

        # Advertising
        self.link.sendto(self.MSG, ('255.255.255.255', self.PORT))
        sleep(self.BEACON)

    def Connect(self, endpoint_ip, endpoint_port):
        """
        Used to setup the TCP connection before sending infos
        """

        # TCP socket initialization
        self.link = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

        # Endpoint connection
        self.link.connect((endpoint_ip, endpoint_port))