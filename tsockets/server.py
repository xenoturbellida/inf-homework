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


clients = []  # all clients connected to the server
nicknames = []  # all nicknames
waiting_rooms = []  # list containing chat rooms that have only 1 member


def handle_client(client, room):
    while True:
        try:
            message = client.recv(1024)

            # if the second client has left the chat, we try to find another client to converse
            if message.decode('ascii') == 'find_new_conversation':
                # if someone is in the waiting list, we assign a room from the waiting list to our room
                if waiting_rooms:
                    waiting_room = waiting_rooms[0]
                    waiting_rooms.remove(waiting_room)
                    waiting_room.room_clients[0].send('new_conversation_found'.encode('ascii'))
                    client.send('new_conversation_found'.encode('ascii'))
                    waiting_room.room_clients.append(client)
                    room = waiting_room
                    continue
                # if the waiting list is empty, the current room goes to the waiting list
                waiting_rooms.append(room)
                client.send('You were added to the waiting list.'.encode('ascii'))
                continue

        # if the client has disconnected, we inform the second client
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

        # get a client from waiting list
        if waiting_rooms:
            waiting_room = waiting_rooms[0]
            waiting_rooms.remove(waiting_room)
            waiting_room.room_clients[0].send('new_conversation_found'.encode('ascii'))
            client.send('New conversation found!'.encode('ascii'))
            waiting_room.room_clients.append(client)
            client_thread = Thread(target=handle_client, args=(client, waiting_room))
            client_thread.start()
        # if the waiting list is empty, we start a new thread
        # where this client will be added to the waiting list
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
