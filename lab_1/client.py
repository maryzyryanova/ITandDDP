import socket
import random
import threading
from functions import readJson

config = readJson()
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((config[0], random.randint(8000, 9000)))
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

client.sendto(f"SIGNUP_TAG:{nickname}".encode(), (config))

while True:
    msg = input("")
    if msg == "!q":
        exit()
    else:
        client.sendto(f"{nickname}: {msg}".encode(), (config))
