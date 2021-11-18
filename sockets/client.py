import threading
import socket


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'move_to_waiting_list':
                client.send(message.encode('ascii'))
            else:
                print(message)
        except socket.error as e:
            print('An error occurred!')
            print(e)
            client.close()
            break


def write():
    while True:
        message = input()
        message_to_send = f'{nickname}: {message}'
        client.send(message_to_send.encode('ascii'))


nickname = input('Choose your nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 50007))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
