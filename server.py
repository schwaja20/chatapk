
"""
import logging


logging.basicConfig(
    filemode='w',
    filename='logserver.log',
    level=logging.DEBUG,
    format='%(asctime)s : %(message)s',
    datefmt='[%Y/%m/%d] %H:%M:%S',
)

logging.info('Startuji server')

logging.info('--> server start OK')

while True:
    logging.info(input(">"))
"""

from tkinter import *
from socket import *
import _thread

# nastaveni spojeni se serverem
def initialize_server():
    # nastaveni sockeru
    s = socket(AF_INET, SOCK_STREAM)

    # detaily
    host = 'localhost'  ## to use between devices in the same network eg.192.168.1.5
    port = 1234

    # pripojeni serveru
    s.bind((host, port))
    s.listen(1)
        #potvrzeni pripojeni
    conn, addr = s.accept()

    return conn

# update a drzeni zprav v chatu
def update_chat(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)
    # pridavani zprav
    if state==0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'OTHER: ' + msg)
    chatlog.config(state=DISABLED)
    # zobrazeni posledni zpravy
    chatlog.yview(END)

# odesilani zprav
def send():
    global textbox
    # ziskani zpravy
    msg = textbox.get("0.0", END)
    # update chatu
    update_chat(msg, 0)
    # odeslani
    conn.send(msg.encode('ascii'))
    textbox.delete("0.0", END)

# prijeti zpravy
def receive():
    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass

def press(event):
    send()

# grafika okna
def GUI():
    global chatlog
    global textbox

    # nastaveni okna
    gui = Tk()
    gui.title("Server Chat")
    gui.geometry("380x430")

    # text space to display messages
    chatlog = Text(gui, bg='white')
    chatlog.config(state=DISABLED)

    # tlacitko odeslat
    sendbutton = Button(gui, bg='white', fg='black', text='SEND', command=send)

    # psani zprav
    textbox = Text(gui, bg='white')

    # pozicovani chatu a zprav
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # bind pro pouziti enteru
    textbox.bind("<KeyRelease-Return>", press)

    # create thread to capture messages continuously
    _thread.start_new_thread(receive, ())

    # loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    conn = initialize_server()
    GUI()


