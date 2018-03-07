import socket, sys
from tkinter import *
import _thread

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
def connect_server(entry_1, entry_2):
        global host
        host = entry_1.get()
        port = int(entry_2.get())

        # connect to remote host
        try :
                s.connect((host, port))
        except :
                write_to_screen("Unable To Connect","")
        write_to_screen("connected to "+ host +":"+str(port),"")
        _thread.start_new_thread(receive, ())

def write_to_screen(text,username):
        global T
        T.config(state=NORMAL)
        T.insert(END, '\n')
        T.insert(END, username+text)
        T.yview(END)
        T.config(state=DISABLED)

def receive():
        global s
        while True:
                data=s.recv(4096)
                if not data: sys.exit()
                write_to_screen(data.decode('utf-8'),host + ' : ')

def send_message():
        global T
        global msg_entry
        msg1 = msg_entry.get()
        write_to_screen(msg1,"self : ")
        msg = msg1.encode('utf-8')
        s.sendall(msg)
        msg_entry.delete(0, END)

root = Tk()
root.title("Client")

topframe = Frame(root)
topframe.pack()
label_1 = Label(topframe, text="Address")
label_2 = Label(topframe, text="Port")
entry_1 = Entry(topframe)
entry_2 = Entry(topframe)
label_1.grid(row=0, column=0, sticky=E)
label_2.grid(row=0, column=2, sticky=E)
entry_1.grid(row=0, column=1)
entry_2.grid(row=0,column=3)
button1 = Button(topframe, text = "connect", fg="green", width=20, command = lambda : connect_server(entry_1,entry_2))
button1.grid(row=1, column=1, columnspan=3)

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