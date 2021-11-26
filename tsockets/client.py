import threading
import socket


block_client = False


def receive():
    global block_client
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'find_new_conversation':
                client.send('find_new_conversation'.encode('ascii'))
                print('We are looking for new conversation...')
                block_client = True
            elif message == 'new_conversation_found':
                print('New conversation found!')
                block_client = False
            else:
                print(message)
        except socket.error:
            print('An error occurred!')
            client.close()
            break


def write():
    global block_client
    while True:
        if not block_client:
            message = input()
            if not block_client:
                message_to_send = f'{nickname}: {message}'
                client.send(message_to_send.encode('ascii'))


nickname = input('Choose your nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 50007))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
