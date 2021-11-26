import threading
import socket


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'finding_new_conversation':
                client.send('finding_new_conversation'.encode('ascii'))
                print('We are looking for new conversation...')
            else:
                print(message)
        except:
            print('An error occurred!')
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