from socket import *
from threading import Thread
from time import sleep, time
from json import loads, dumps
from json.decoder import JSONDecodeError
from os import stat

def getlocalips() -> tuple:
    # Returns IP list for each machine's NIC
    return tuple(gethostbyname_ex(gethostname())[2])

class Controller():
    """
    TCP data transmission with UDP device advertising
    """

    # Thread flags
    is_scanning = False
    is_broadcasting = False
    
    # Socket objects
    server = socket()
    broadcaster = socket()

    # Detected devices list
    nearby_devices = {}
    
    def __init__(self, hostname = gethostname(), ip = getlocalips()[0],
                 service_port = 5000, advertising_port = 5555,
                 max_clients = 5, beacon = 1, timeout = 10, bufsize = 4096) -> None:
        
        self.host = hostname if hostname != None else gethostname()
        self.server_port = service_port
        
        self.MSG = bytes(
            dumps({
                "name": gethostname(),
                "port": str(self.server_port)
            }),
            'utf-8'
        )

        self.broadcast_port = advertising_port
        self.localip = ip
        self.max_clients = max_clients
        self.beacon = beacon
        self.timeout = timeout
        self.bufsize = bufsize

    def Receive_States(self):
        """
        Send broadcast message and receive file
        """

        # Socket setup
        self._udp_setup()

        # Advertising with daemon thread
        self.broadcast_thread = Thread(name = 'Advertising', target = self._broadcast, daemon = True)
        self.broadcast_thread.start()

        self.serve_thread = Thread(name = 'Server', target = self.receive)
        self.serve_thread.start()
        # self.serve_thread.join()

    def _broadcast(self):
        self.is_broadcasting = True

        while self.is_broadcasting:
            self.broadcaster.sendto(self.MSG, ('255.255.255.255', self.broadcast_port))
            sleep(self.beacon)

    def receive(self):
        """
        Wait for receivers to connect and get data
        """

        # Close any open socket on that port
        self.server.close()

        # TCP socket initialization
        self.server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

        # Address binding
        self.server.bind((self.localip, self.server_port))

        # Listening for connections
        self.server.listen(self.max_clients)

        # Stop broadcasting to start transferring
        self.is_broadcasting = False

        # Accept incoming connections
        client, endpoint = self.server.accept()

        # Receiving vars
        headers = b''
        data = b''
        buffer = b''

        # Get headers
        while not (b'\x00' in buffer):
            buffer = client.recv(self.bufsize)
            headers += buffer
        
        # Some data could be there yet
        headers, data = str(headers, 'utf-8').split('\x00')

        '''
        Header Parser - Format:
        {
            "size": 10,
            "filename": ""
        }
        '''
        try:
            headers = loads(headers)
        except JSONDecodeError as e:
            raise error("Unable to decode JSON headers" + str(e))
        
        is_file = (headers['filename'] == '')
        data_left = headers['size']

        # If file, open output file
        # else, data will be stored in data var
        if is_file:
            output = open(headers['filename'], 'wb')

            # Write bytes that came after headers
            output.write(data)

        # Get data
        while data_left > 0:
            buffer = client.recv(self.bufsize)
            if is_file:
                output.write(buffer)
            else:
                data += buffer
            data_left -= self.bufsize

        if is_file: output.close()

        # Close socket at the end
        self.server.close()

    def send(self, data, content = 'string'):
        """
        Sends data to the receiving socket
        data: text | filepath
        type: file | string
        """

        # Param check
        if not (content in ('file', 'string')):
            raise ValueError("type argument must be 'file' or 'string'")

        is_file = (content == 'file')

        # Setup TCP socket
        self._tcp_setup()

        # Init connection - we need to set
        # the receiver before doing so
        self.server.connect(self.selected_receiver)

        # Headers setup
        headers = {}

        if is_file:
            headers["size"] = stat(data).st_size
            headers["filename"] = data
        else:
            headers["size"] = len(data)
            headers["filename"] = ''

        # Open file
        if is_file:
            file = open(data, 'rb')

        # Send headers -- INCOMPLETE
        self.server.sendall(headers)

        # End of headers
        self.server.send(bytes(1))

        # Send data
        data_left = headers['size']

        while data_left > 0:
            if is_file:
                self.server.send(file.read(self.bufsize))
            else:
                # Send all data in one time
                self.server.sendall(data)
                break

        if is_file: file.close()
        
        # Close socket after all
        self.server.close()

    def scan(self):
        """
        Scans for broadcasting receivers in the local network
        """

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

        # Do it better with a mutex thing
        self.is_scanning = True
        
        # Start scan manager daemon
        Thread(target=self._scan_manager, daemon=True).start()

        # Socket setup
        self._udp_setup()

        # Scanner
        while self.is_scanning:
            # Receive broadcast message
            payload, endpoint = self.broadcaster.recvfrom(self.bufsize)
            
            # Decode and parse payload
            data = loads(str(payload, 'utf-8'))

            # Save new device
            self.nearby_devices[endpoint[0]] = {
                'hostname': data['name'],
                'port': data['port'],
                'last_beacon': time()
            }
        
    def _scan_manager(self):
        """
        Grants data integrity in devices list
        """

        while self.is_scanning:
            for ip, info in self.nearby_devices.items():
                if (info['last_beacon'] + self.timeout) < time():
                    # Remove devices whose last beacon is too old
                    self.nearby_devices.pop(ip)
            sleep(self.timeout)
    
    def _udp_setup(self):
        """
        Setup socket before broadcasting
        """

        # Close any open socket on that port
        self.broadcaster.close()

        # Setup UDP broadcasting
        self.broadcaster = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.broadcaster.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # IP address binding
        self.broadcaster.bind((self.localip, self.broadcast_port))

    def _tcp_setup(self):
        """
        Used to setup the TCP sockets
        """

        # Close any open socket on that port
        self.server.close()

        # TCP socket initialization
        self.server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

        # Address binding
        self.server.bind((self.localip, self.server_port))