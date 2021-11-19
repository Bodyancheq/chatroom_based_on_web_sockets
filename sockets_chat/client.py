import socket
import sys
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!disconnect'
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def listen():
    while True:
        msg = client.recv(2048).decode(FORMAT)
        print(msg)


def send():
    while True:
        message = input()
        client.send(message.encode(FORMAT))



if __name__ == '__main__':
    thread = threading.Thread(target=listen,daemon=True)
    thread.start()
    while True:
        message = input()
        client.send(message.encode(FORMAT))
        if message == DISCONNECT_MESSAGE:
            sys.exit()
