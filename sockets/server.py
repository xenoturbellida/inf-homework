import socket
import threading


HOST = '127.0.0.1'
PORT = 50007


def send_message(message, mate_ind):
    clients[mate_ind].send(message)


def handle(client):
    while True:
        index = clients.index(client)
        mate_index = (index + 1) if (index % 2 == 0) else index - 1
        try:
            message = client.recv(1024)
            send_message(message, mate_index)
        except socket.error:
            del clients[index]
            client.close()
            nickname = nicknames[index]
            send_message(f'{nickname} left!'.encode('ascii'), mate_index)
            del nicknames[index]
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
            current_client_thread = threading.Thread(target=handle, args=(client,))
            current_client_thread.start()

            prev_client = clients[-2]
            prev_client_thread = threading.Thread(target=handle, args=(prev_client,))
            prev_client_thread.start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

receive()
