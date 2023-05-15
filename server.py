from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_connections():
    while True:
        client_socket, client_address = server.accept()
        print('%s:%s is now connected.' % client_address)
        client_socket.send(bytes('Type your Name', 'utf8'))
        addresses[client_socket] = client_address
        Thread(target=client_communication, args=(client_socket,)).start()

def client_communication(client_socket):
    name = client_socket.recv(size).decode('utf8')
    welcome = 'Welcome %s! To leave, type (quit)' % name
    client_socket.send(bytes(welcome, 'utf8'))
    msg = '%s has joined the chat!' % name
    broadcast(bytes(msg, 'utf8'))
    clients[client_socket] = name

    while True:
        msg = client_socket.recv(size)
        if msg != bytes('(quit)', 'utf8'):
            broadcast(msg, name + ': ')
        else:
            client_socket.send(bytes('(quit)', 'utf8'))
            client_socket.close()
            del clients[client_socket]
            broadcast(bytes('%s has left the chat.' % name, 'utf8'))
            break

def broadcast(msg, prefix=''):
    for sock in clients:
        sock.send(bytes(prefix, 'utf-8') + msg)

host = 'localhost'
port = 8888
size = 512
addr = (host, port)
clients = {}
addresses = {}

server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

server.listen(3)
print('The chat is open')
handle_connections = Thread(target=accept_connections())
handle_connections.start()
handle_connections.join()
server.close()