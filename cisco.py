import socket
from os import chdir

chdir("C:\\Users\\gugli\\Downloads")

def ricevi_comandi(conn):
    file_cisco = open("sock.py", "rb")
    while True:
        byte_letti = file_cisco.read(4096)
        if not byte_letti:
            break
        conn.sendall(byte_letti)
    file_cisco.close()


def sub_server(indirizzo, backlog=1):
    try:
        s = socket.socket()
        s.bind(indirizzo)
        s.listen(backlog)
        print("Server Inizializzato. In ascolto...")
    except socket.error as errore:
        print(f"Qualcosa è andato storto... \n{errore}")
        print(f"Sto tentando di reinizializzare il server...")
        sub_server(indirizzo, backlog=1)
    conn, indirizzo_client = s.accept() #conn = socket_client
    print(f"Connessione Server - Client Stabilita: {indirizzo_client}")
    ricevi_comandi(conn)


if __name__ == '__main__':
    sub_server(("192.168.137.138", 20000))

