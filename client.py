import socket 
import threading
import os
import tkinter
import time

target_host = "192.168.0.108"
target_port = 8080

os.system('clear')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

def send_message_event(event):
    message = entry.get()
    client.send(message.encode("utf-8"))
    entry.delete(0, tkinter.END)

def send_message():
    message = entry.get()
    client.send(message.encode("utf-8"))
    entry.delete(0, tkinter.END)

window = tkinter.Tk()
window.title("LAN Chat")
scrollbar = tkinter.Scrollbar(window)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
chat_box = tkinter.Text(window, height=25, width=50)
chat_box.pack(fill=tkinter.X)
scrollbar.config(command=chat_box.yview)
chat_box.config(yscrollcommand=scrollbar.set)
entry = tkinter.Entry(window, width=30)
entry.pack()
entry.bind('<Return>', send_message_event)
button = tkinter.Button(window, text="Enviar", width=15, command=send_message)
button.pack()

def handle_server():
    while True:
        res = client.recv(4096).decode("utf-8")
        if res=="":
            break
        print(res)    
        chat_box.insert(tkinter.END, res)

handler = threading.Thread(target=handle_server, daemon=True)
handler.start()

window.mainloop()

"""while True:
    try:
        mess = input("")
        client.send(mess.encode("utf-8"))
    except:
        print("A conexão foi fechada.")
        break"""

