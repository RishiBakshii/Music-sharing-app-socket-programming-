import socket
import threading


SERVER=None
IP_ADDRESS='127.0.0.1'
PORT=8050
BUFFER_SIZE=4096
clients={}


def accept_connections():
    global SERVER,clients
    
    while True:
        client,addr=SERVER.accept()
        print(f'Connection established with {client} {addr[0]}')

def setup():
    global PORT,IP_ADDRESS,SERVER

    SERVER=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))

    SERVER.listen(100)
    print("Server is waiting for incoming connections\n\n")

    accept_connections()

threading.Thread(target=setup).start()


