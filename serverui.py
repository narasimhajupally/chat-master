import socket, sys
from tkinter import *
import _thread
 
HOST = ''   # Symbolic name meaning all available interfaces
address = []
connections = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def host_server(entry_1):
        global HOST
        PORT = int(entry_1.get())
        try:
                write_to_screen("Hosted Succesfully, Waiting for Client...","")
                s.bind((HOST, PORT))
        except (socket.error , msg):
                write_to_screen('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1],"")
        
        s.listen(10) 
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        connections.append(conn)
        address.append(addr[0])
        #display client information
        write_to_screen('Connected with ' + addr[0] + ':' + str(addr[1]),"")
        _thread.start_new_thread(receive, ())

def write_to_screen(text,username):
        global T
        T.config(state=NORMAL)
        T.insert(END, '\n')
        T.insert(END, username+text)
        T.yview(END)
        T.config(state=DISABLED)

def receive():
        global connections
        while True:
                data=connections[0].recv(4096)
                if not data: sys.exit()
                write_to_screen(data.decode('utf-8'), '<'+address[0]+'> : ')

def send_message():
        global T
        global msg_entry
        msg1 = msg_entry.get()
        write_to_screen(msg1,"self : ")
        msg = msg1.encode('utf-8')
        connections[0].sendall(msg)
        msg_entry.delete(0, END)


root = Tk()
root.title("Server")

topframe = Frame(root)
topframe.pack()
label_1 = Label(topframe, text="Port")
entry_1 = Entry(topframe)
label_1.grid(row=0, column=0, sticky=E)
entry_1.grid(row=0, column=1)
button1 = Button(topframe, text = "Launch", fg="green", width=20, command = lambda : host_server(entry_1))
button1.grid(row=1, column=1)

body = Frame(root)
S = Scrollbar(body)
T = Text(body, height=20, width=60)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=X)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = "Welcome"
body.pack()
T.insert(END, quote)
T.config(state=DISABLED)

bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM, fill=BOTH)
msg_entry = Entry(bottomframe, width=40)
msg_entry.grid(row=0, column=0, ipady=10, sticky=W)
send_button = Button(bottomframe, text = "send", fg="green", height=2, width=10, command=lambda : send_message())
send_button.grid(row=0, column=1, sticky=E)

root.mainloop()
