import json
import socket
import queue
import threading
from functions import readJson

config = readJson()
messages = queue.Queue()
clients = []
users = []
mess = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(config)

def recievePackage() -> None:
    while True:
        try:
            messages.put(server.recvfrom(1024))
        except:
            pass

def broadcastFunction() -> None:
    id = 0
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
                        users.append(nickname)
                        server.sendto(f"{nickname} online!".encode(), client)
                    else:
                        server.sendto(msg, client)
                except:
                    clients.remove(client)
            if msg.decode().startswith("SIGNUP_TAG:"):
                mess.append({"id" : id, "sender" : nickname, "text" : f"{nickname} online!"})
            else:
                mess.append({"id" : id, "sender" : nickname, "text" : msg.decode()})
            id += 1
            print(mess)
        with open('messages.json', 'w') as f:
            json.dump({"chat_id" : 1, "users" : users, "messages" : mess}, f)



thread_1 = threading.Thread(target=recievePackage)
thread_2 = threading.Thread(target=broadcastFunction)

thread_1.start()
thread_2.start()