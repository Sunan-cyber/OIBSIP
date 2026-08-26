#Oasis Infobyte Internship programme Python Programming building Chatapplication

import socket #import required modules
import threading
from datetime import datetime
#Server configuration

HOST = "127.0.0.1" #LOCALHOST address
PORT = 5555 #Port used for communication
#variable for client and their username
clients = []
names = []

#generate the current time stamp for message timestamps
def timestamp():
    return datetime.now().strftime("%H:%M")

#messages sent to all connected clients
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                pass


def handle_client(client, name):
    try:
        while True:
            message = client.recv(1024).decode()

            if not message:
                break

            formatted_message = f"[{timestamp()}] {name}: {message}"
            print(formatted_message)

            broadcast(formatted_message, client)

    except ConnectionResetError:
        pass

    finally:
        if client in clients:
            clients.remove(client)

        if name in names:
            names.remove(name)

        client.close()

        broadcast(f"[{timestamp()}] {name} has disconnected.")

        print(f"{name} disconnected.")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)

    print("Server started.")
    print(f"Waiting for clients on {HOST}:{PORT}...")

    while len(clients) < 2:
        client, address = server.accept()

        client.send("NAME".encode())
        name = client.recv(1024).decode()

        clients.append(client)
        names.append(name)

        print(f"{name} connected from {address}")

        client.send(
            f"[{timestamp()}] Connected to the chat.".encode()
        )

        if len(clients) == 2:
            broadcast(f"[{timestamp()}] Both users are connected. Chat started.")

        thread = threading.Thread(
            target=handle_client,
            args=(client, name)
        )
        thread.start()

    print("Two clients connected. Server is now full.")


start_server()
