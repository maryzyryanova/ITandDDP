import socket
import random
import threading
from . import config

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((config.HOST, random.randint(8000, 9000)))
nickname = input("Nickname: ")

def recievePackage() -> None:
    while True:
        try:
            msg, adr = client.recvfrom(1024)
            print(msg.decode())
        except:
            pass

thr = threading.Thread(target=recievePackage)
thr.start()

client.sendto(f"SIGNUP_TAG:{nickname}".encode(), (config.HOST, config.PORT))

while True:
    msg = input("")
    if msg == "!q":
        exit()
    else:
        client.sendto(f"{nickname}: {msg}".encode(), (config.HOST, config.PORT))
