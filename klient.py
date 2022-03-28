"""
client_socket = socket.socket()
klient = socket.gethostname
port = 12345
try:
    client_socket.connect((klient, port))
"""

from tkinter import *
from socket import *
import _thread


# nastaveni spojeni se serverem
def klient_start():
    # nastaveni sockeru
    s = socket(AF_INET, SOCK_STREAM)

    # detaily
    host = 'localhost'
    port = 1234

    # pripojeni
    s.connect((host, port))

    return s


# update a drzeni zprav v chatu
def chat_update(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)
    # pridavani zprav
    if state == 0:
        chatlog.insert(END, 'VY: ' + msg)
    else:
        chatlog.insert(END, 'THOTKA: ' + msg)
    chatlog.config(state=DISABLED)
    # zobrazeni posledni zpravy
    chatlog.yview(END)


# odesilani zprav
def odeslat():
    global textbox
    # ziskani zpravy
    msg = textbox.get("0.0", END)
    # update chatu
    chat_update(msg, 0)
    # odeslani
    s.send(msg.encode('ascii'))
    textbox.delete("0.0", END)


# prijeti zpravy
def receive():
    while 1:
        try:
            data = s.recv(1024)
            msg = data.decode('UTF-8')
            if msg != "":
                chat_update(msg, 1)
        except:
            pass


def press(event):
    odeslat()


# grafika okna
def GUI():
    global chatlog
    global textbox

    # nastaveni okna
    gui = Tk()
    gui.title("Lide.cz - Client Chat")
    gui.geometry("380x430")

    # zobrazeni textu
    chatlog = Text(gui, bg='white')
    chatlog.config(state=DISABLED)

    # tlacitko odeslat
    sendbutton = Button(gui, bg='white', fg='black', text='SEND', command=odeslat)

    # psani zprav
    textbox = Text(gui, bg='white')

    # pozicovani chatu a zprav
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # bind pro pouziti enteru
    textbox.bind("<KeyRelease-Return>", press)

    # zachytavani zprav
    _thread.start_new_thread(receive, ())

    # loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    s = klient_start()
    GUI()