import socket
from threading import Thread, Lock


HOST = '127.0.0.1'
PORT = 50007


def send_message(message, mate):
    mate.send(message)


def handle(client, mate):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('ascii') == 'move_to_waiting_list':
                waiting_list.append(mate)
                mate.send('Waiting for the next mate...'.encode('ascii'))
                break
        except socket.error:
            client.close()
            index = clients.index(client)
            nickname = nicknames[index]
            mate.send(f'{nickname} left!'.encode('ascii'))
            mate.send('move_to_waiting_list'.encode('ascii'))

            del nicknames[index]
            del clients[index]
            break
        try:
            mate.send(message)
        except socket.error:
            waiting_list.append(mate)
            mate.send('Waiting for the next mate...'.encode('ascii'))
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname is {nickname}')
        client.send('Connected to server'.encode('ascii'))

        if len(clients) % 2 == 0:
            client2 = waiting_list[0]
            del waiting_list[0]

            client_thread = Thread(target=handle, args=(client, client2))
            client_thread.start()
            print('started new thread client 1')

            client2_thread = Thread(target=handle, args=(client2, client))
            client2_thread.start()
            print('started new thread client 2')
        else:
            waiting_list.append(client)


def serve_waiting_list(lock):
    while True:
        lock.acquire()
        print('checking the queue')
        if waiting_list and len(waiting_list) % 2 == 0:
            client1_thread = Thread(target=handle, args=(waiting_list[0], waiting_list[1]))
            client2_thread = Thread(target=handle, args=(waiting_list[1], waiting_list[0]))
            client1_thread.start()
            client2_thread.start()
            del waiting_list[0]
            del waiting_list[1]
        lock.release()


clients = []
nicknames = []
waiting_list = []


thread_lock = Lock()

serve_waiting_list_thread = Thread(target=serve_waiting_list, args=(thread_lock,))
serve_waiting_list_thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Server is running')

receive()
