import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def receive():
    while True:
        try:
            msg = client_socket.recv(size).decode("utf8")
            messages.insert(tkinter.END, msg)
        except OSError:
            break

def send_message(event=None):
    msg = my_msg.get()
    my_msg.set('')
    client_socket.send(bytes(msg, "utf8"))
    if msg == '(quit)':
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_msg.set('(quit)')
    send_message()

top = tkinter.Tk()
top.title("Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)
messages = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send_message)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send_message)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

host = 'localhost'
port = 8888

size = 512
addr = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(addr)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
