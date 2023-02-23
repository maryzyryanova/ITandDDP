import socket
import queue
import threading
from functions import readJson

config = readJson()
messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(config)

def recievePackage() -> None:
    while True:
        try:
            messages.put(server.recvfrom(1024))
        except:
            pass


def broadcastFunction() -> None:
    while True:
        while not messages.empty():
            msg, adr = messages.get()
            print(msg.decode())
            if adr not in clients:
                clients.append(adr)
            for client in clients:
                try:
                    if msg.decode().startswith("SIGNUP_TAG:"):
                        nickname = msg.decode()[msg.decode().index(":")+1:]
                        server.sendto(f"{nickname} joined the chat!".encode(), client)
                    else:
                        server.sendto(msg, client)
                except:
                    clients.remove(client)

thread_1 = threading.Thread(target=recievePackage)
thread_2 = threading.Thread(target=broadcastFunction)

thread_1.start()
thread_2.start()