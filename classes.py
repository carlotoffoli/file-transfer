from socket import *
from threading import Thread, Lock
from time import sleep


class Controller():
    """
    TCP data transmission with UDP device advertising
    """

    lock = Lock()
    
    server = socket()
    broadcaster = socket()

    devices = {}

    LOCALIP = '0.0.0.0'
    PORT_SERVER = 5000
    PORT_BROADCAST = 5555
    MSG = bytes(gethostname()+str(PORT_SERVER), 'utf-8')
    MAX_CONNECTIONS = 5
    BEACON = 1
    SIZE = 4096
    
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

        # Socket setup
        self._setup_broadcast()

        # Advertising with daemon thread
        self.broadcast_thread = Thread(name = 'Advertising', target = self._broadcast, daemon = True)
        self.broadcast_thread.start()
    
    def _setup_broadcast(self):
        """
        Setup socket before broadcasting
        """

        # Close any open socket
        self.broadcaster.close()

        # Setup UDP broadcasting
        self.broadcaster = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.broadcaster.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # IP address binding
        self.broadcaster.bind((self.LOCALIP, self.PORT_BROADCAST))

    def _broadcast(self):
        self.lock.acquire()

        while self.lock.locked():
            self.broadcaster.sendto(self.MSG, ('255.255.255.255', self.PORT_BROADCAST))
            sleep(self.BEACON)

    def _server(self):
        # Close any open socket on that port
        self.server.close()

        # TCP socket initialization
        self.server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

        # Address binding
        self.server.bind((self.LOCALIP, self.PORT_SERVER))

        # Listening for connections
        self.server.listen(self.MAX_CONNECTIONS)

        # Accept incoming connections
        client, endpoint = self.server.accept()

    def _scan(self):
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
        
        # Do it better with a mutex semaphore
        self.lock.acquire()

        # Socket setup
        self._setup_broadcast()

        # 



    def Connect(self, endpoint_ip, endpoint_port):
        """
        Used to setup the TCP connection before sending infos
        """

        # Endpoint connection
        self.server.connect((endpoint_ip, endpoint_port))
        pass