import socket
import threading
import sys
import os

bind_ip = "0.0.0.0"
bind_port = 8080

os.system('clear')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(4)

clients = [None] * 4
addrs   = [None] * 4
names   = [None] * 4
qtd_clients = 0

def broadcast(request, sender):
    print(request.decode("utf-8"))
    for client in clients:
        if(client != None and client != sender):
            client.send(request)

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        #checks if client has disconnected
        if not request:
            break
        if request is not None and request:
            for i in range(4):
                if clients[i] == client_socket:
                    message = names[i].decode("utf-8") + ": " + request.decode("utf-8")
                    broadcast(message.encode("utf-8"), client_socket)

def handle_asker(client_socket, qtd_clients):
    req_message = "Identifique-se:"
    client_socket.send(req_message.encode("utf-8"))
    res = client_socket.recv(1024)
    while res is None:
        res = client_socket.recv(1024)
    names[qtd_clients] = res
    log_entrada = names[qtd_clients].decode("utf-8") +  " acabou de entrar na conversa."
    broadcast(log_entrada.encode("utf-8"), client_socket)
    log_entrada = "Agora você está online, " + names[qtd_clients].decode("utf-8") + "."
    client_socket.send(log_entrada.encode("utf-8"))

while True: 
    if(qtd_clients<4):
        clients[qtd_clients], addrs[qtd_clients] = server.accept()
        qtd_clients+=1
        name_asker_handler = threading.Thread(target=handle_asker, args=(clients[qtd_clients-1], qtd_clients-1, ), daemon=True)
        name_asker_handler.start()
        while(name_asker_handler.isAlive()):
            continue     
        client_handler = threading.Thread(target=handle_client, args=(clients[qtd_clients-1],), daemon=True)
        client_handler.start()

    
