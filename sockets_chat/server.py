import socket
import threading

HEADER = 64
PORT = 5050
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
MSG_LEN = 2048
DISCONNECT_MESSAGE = '!disconnect'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


rooms = []
for i in range(100):
    rooms.append([None, None])


def find_room(conn):
    for room_id, room in enumerate(rooms):
        if (not room[0]) or (not room[1]):
            return room_id


def remove_user_from_room(conn, usr_room_id):
    if rooms[usr_room_id][0] == conn:
        rooms[usr_room_id][0] = None
        rooms[usr_room_id][1].send("Your roommate has left".encode(FORMAT))
    elif rooms[usr_room_id][1] == conn:
        rooms[usr_room_id][1] = None
        rooms[usr_room_id][0].send("Your roommate has left".encode(FORMAT))
    return True


def send_message_to_roommate(usr_room_id, conn, msg):
    if rooms[usr_room_id][0] != conn and rooms[usr_room_id][0]:
        rooms[usr_room_id][0].send(f"---{msg}".encode(FORMAT))
    elif rooms[usr_room_id][1] != conn and rooms[usr_room_id][1]:
        rooms[usr_room_id][1].send(f"---{msg}".encode(FORMAT))


def check_users(usr_room_id):
    if rooms[usr_room_id][0] and rooms[usr_room_id][1]:
        return 1
    return 0


def connect_to_the_room(room_id, conn):
    if rooms[room_id][0]:
        rooms[room_id][1] = conn
    else:
        rooms[room_id][0] = conn
    for user in rooms[room_id]:
        if user and user != conn:
            user.send("You have a roommate now!".encode(FORMAT))


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    usr_room_id = find_room(conn)
    connect_to_the_room(usr_room_id, conn)
    conn.send(f"You have been connected to room {usr_room_id}, there is "
              f"{check_users(usr_room_id)} users beside you\n".encode(FORMAT))
    connected = True
    while connected:
        msg = conn.recv(MSG_LEN).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            remove_user_from_room(conn, usr_room_id)
            conn.send("Disconnecting...".encode(FORMAT))
            conn.close()
        else:
            send_message_to_roommate(usr_room_id, conn, msg)
        print(msg)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


print('[STARTING] server is starting...')
start()
