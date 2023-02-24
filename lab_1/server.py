import json
import socket
import queue
import threading
from functions import readJson

config = readJson()
messages = queue.Queue()
clients = []
users = set()
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
            message = msg.decode()
            print(message)
            if adr not in clients:
                clients.append(adr)
            for client in clients:
                try:
                    if message.startswith("SIGNUP_TAG:"):
                        nickname = message[message.index(":")+1:]
                        server.sendto(f"{nickname} online!".encode(), client)
                        users.add(nickname)
                    else:
                        server.sendto(msg, client)
                except:
                    clients.remove(client)
                if message.startswith("SIGNUP_TAG:"):
                    nickname = message[message.index(":")+1:]
                    mess.append({"id" : id, "sender" : nickname, "text" : f"{nickname} online!"})
                else:
                    nickname = message[0:message.index(":")]
                    mess.append({"id" : id, "sender" : nickname, "text" : message})
                id += 1
                print(mess)
                print(users)
            with open('messages.json', 'w+') as f:
                json.dump({"chat_id" : 1, "users" : list(users), "messages" : mess}, f)

thread_1 = threading.Thread(target=recievePackage)
thread_2 = threading.Thread(target=broadcastFunction)

thread_1.start()
thread_2.start()