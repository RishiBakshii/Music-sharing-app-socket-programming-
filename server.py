import socket
import threading


SERVER=None
IP_ADDRESS='127.0.0.1'
PORT=8050
BUFFER_SIZE=4096
clients={}


def handle_client(client,client_name):
    client.send("welcome to the server you have connected succesfully".encode("utf-8"))

def accept_connections():
    global SERVER,clients
    
    while True:
        client,addr=SERVER.accept()
        client_name=client.recv(4096).deocde().lower()
        clients[client_name]={
            'client':client,
            'address':addr,
            'connected_with':'',
            'file_name':'',
            'file_size':BUFFER_SIZE
        }
        print(f'Connection established with {client_name} {addr[0]}')

        threading.Thread(target=handle_client,args=(client,client_name)).start()

def setup():
    global PORT,IP_ADDRESS,SERVER

    SERVER=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))

    SERVER.listen(100)
    print("Server is waiting for incoming connections\n\n")

    accept_connections()

threading.Thread(target=setup).start()


