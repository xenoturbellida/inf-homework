import socket
from threading import Thread


class Room:
    def __init__(self, room_clients: list):
        self.room_clients = room_clients

    def get_mate(self, client):
        if len(self.room_clients) > 1:
            mate_ind = (self.room_clients.index(client) + 1) % 2
            mate = self.room_clients[mate_ind]
            return mate


clients = []
nicknames = []
waiting_rooms = []


def handle_client(client, room):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('ascii') == 'find_new_conversation':
                if waiting_rooms:
                    waiting_room = waiting_rooms[0]
                    waiting_rooms.remove(waiting_room)
                    waiting_room.room_clients[0].send('new_conversation_found'.encode('ascii'))
                    client.send('new_conversation_found'.encode('ascii'))
                    waiting_room.room_clients.append(client)
                    room = waiting_room
                    continue
                waiting_rooms.append(room)
                client.send('You were added to the waiting list.'.encode('ascii'))
                continue
        except socket.error:
            client.close()
            index = clients.index(client)
            nickname = nicknames[index]

            mate = room.get_mate(client)

            if mate:
                mate.send(f'{nickname} left!'.encode('ascii'))
                mate.send('find_new_conversation'.encode('ascii'))

            del nicknames[index]
            del clients[index]
            room.room_clients.remove(client)

            print(f"{nickname} has left the chat. Current number of clients: {len(clients)}")

            break

        mate = room.get_mate(client)
        if mate:
            mate.send(message)


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname is {nickname}')
        print(f"Current number of clients: {len(clients)}")
        client.send('Connected to server'.encode('ascii'))

        if waiting_rooms:
            waiting_room = waiting_rooms[0]
            waiting_rooms.remove(waiting_room)
            waiting_room.room_clients[0].send('new_conversation_found'.encode('ascii'))
            client.send('New conversation found!'.encode('ascii'))
            waiting_room.room_clients.append(client)
            client_thread = Thread(target=handle_client, args=(client, waiting_room))
            client_thread.start()
        else:
            client_thread = Thread(target=handle_client, args=(client, Room([client])))
            client_thread.start()
            client.send('find_new_conversation'.encode('ascii'))


HOST = '127.0.0.1'
PORT = 50007

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Server is running')

receive()
