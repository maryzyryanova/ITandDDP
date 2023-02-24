import json

def readJson():
    with open("config.json", "r") as config:
        developer = json.load(config)
        host = developer["HOST"]
        port = developer["PORT"]
    return (host, port)
