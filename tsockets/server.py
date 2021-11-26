import socket
from threading import Thread


class Room:
    def __init__(self, room_clients: list):
        self.room_clients = room_clients

    def get_mate(self, client):
        if len(self.room_clients) > 1:
            mate_ind = (self.room_clients.index(client) + 1) % 2
            mate = self.room_clients[mate_ind]

            # print(nicknames[clients.index(client)], ': mate ', mate, nicknames[clients.index(mate)])

            return mate

    def size(self):
        return len(self.room_clients)


clients = []
nicknames = []
waiting_client = None
waiting_rooms = []


def handle_client(client, room):
    global waiting_client
    while True:

        # print(nicknames[clients.index(client)], ': waiting rooms ', waiting_rooms)
        # print(nicknames[clients.index(client)], ': room clients ', room.room_clients)

        """
                find_new_conversation = room.size() < 2
        
                if find_new_conversation:
                    if room not in waiting_rooms:
                        # print(nicknames[clients.index(client)], ': current waiting rooms (0) ', waiting_rooms)
                        waiting_rooms.append(room)
                        # print(nicknames[clients.index(client)], ': adding to waiting rooms (1) ', waiting_rooms)
        
                    for waiting_room in waiting_rooms:
                        if waiting_room != room:
                            if room in waiting_rooms:
                                waiting_rooms.remove(room)
                            waiting_rooms.remove(waiting_room)
                            room = waiting_room
                            room.room_clients.append(client)
                            client.send('New conversation found!'.encode('ascii'))
                            break
        
                    continue
        """

        print(nicknames[clients.index(client)], ': waiting rooms ', waiting_rooms)

        try:
            message = client.recv(1024)
            print(nicknames[clients.index(client)], ' : message : ', message.decode('ascii'))
            if message.decode('ascii') == 'new_conversation_found':
                continue
            if message.decode('ascii') == 'find_new_conversation':
                if waiting_rooms:
                    waiting_room = waiting_rooms[0]
                    waiting_rooms.remove(waiting_room)
                    waiting_room.room_clients[0].send('New conversation found!'.encode('ascii'))
                    waiting_room.room_clients[0].send('new_conversation_found'.encode('ascii'))
                    client.send('New conversation found!'.encode('ascii'))
                    client.send('new_conversation_found'.encode('ascii'))

                    waiting_room.room_clients.append(client)
                    room = waiting_room
                    continue
                waiting_rooms.append(room)
                client.send('You were added to the waiting list'.encode('ascii'))
                continue
        except:
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
            print(nickname, ' has left. all clients: ', clients)

            break

        mate = room.get_mate(client)

        try:
            mate.send(message)
        except:
            continue
            # if room not in waiting_rooms:
            #     waiting_rooms.append(room)
            # # print('exception while sending a message')
            #     print(nicknames[clients.index(client)], ': adding to waiting rooms (2) ', waiting_rooms)


def receive():
    global waiting_client

    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname is {nickname}')
        client.send('Connected to server'.encode('ascii'))

        print('waiting rooms ', waiting_rooms)

        print('all clients: ', clients)

        if waiting_rooms:
            waiting_room = waiting_rooms[0]
            waiting_rooms.remove(waiting_room)
            waiting_room.room_clients[0].send('New conversation found!'.encode('ascii'))
            waiting_room.room_clients[0].send('new_conversation_found'.encode('ascii'))
            client.send('New conversation found!'.encode('ascii'))
            waiting_room.room_clients.append(client)
            # print('client addr ===========', client)
            client_thread = Thread(target=handle_client, args=(client, waiting_room))
            client_thread.start()
        else:
            client_thread = Thread(target=handle_client, args=(client, Room([client])))
            client_thread.start()
            client.send('find_new_conversation'.encode('ascii'))

        """
        if len(clients) % 2 == 0:
            if waiting_rooms:
                waiting_room = waiting_rooms[0]
                del waiting_rooms[0]
                waiting_room.room_clients[0].send('New conversation found!'.encode('ascii'))
                waiting_room.room_clients.append(client)
                print('client addr ===========', client)
                client_thread = Thread(target=handle_client, args=(client, waiting_room))
                client_thread.start()
            else:
                print("!!!!!   Incorrect clients' number   !!!!!!")
        else:
            client.send('Looking for conversation...'.encode('ascii'))
            client_thread = Thread(target=handle_client, args=(client, Room([client])))
            client_thread.start()
        

            
            if waiting_rooms:
                waiting_room = waiting_rooms[0]
                del waiting_rooms[0]
                waiting_room.room_clients.append(client)
                print('client addr ===========', client)
                client_thread = Thread(target=handle_client, args=(client, waiting_room))
                client_thread.start()
            elif waiting_client:
                room = Room([client, waiting_client])
                waiting_client_thread = Thread(target=handle_client, args=(waiting_client, room))
                client_thread = Thread(target=handle_client, args=(client, room))

                waiting_client_thread.start()
                client_thread.start()

                waiting_client = None
            else:
                print("Incorrect clients' number")
       else:
            waiting_client = client         
                
        """


HOST = '127.0.0.1'
PORT = 50007

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Server is running')

receive()
