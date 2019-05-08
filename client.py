import socket 
import threading
import os

target_host = "192.168.0.108"
target_port = 8080

os.system('clear')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
    
def handle_server():
    while True:
        res = client.recv(4096).decode("utf-8")
        if res=="":
            break
        print(res)

handler = threading.Thread(target=handle_server, daemon=True)
handler.start()

while True:
    try:
        mess = input("")
        client.send(mess.encode("utf-8"))
    except:
        print("A conexão foi fechada.")
        break

