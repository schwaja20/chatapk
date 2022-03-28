
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
import logging

#logging
logging.basicConfig(
    filename='server_log.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s : %(message)s',
    datefmt='[%d/%m/%Y] %H:%M:%S'
)


# nastaveni spojeni se serverem
def server_start():
    # nastaveni sockeru
    s = socket(AF_INET, SOCK_STREAM)

    # detaily
    host = 'localhost'
    port = 1234

    # pripojeni serveru
    s.bind((host, port))
    s.listen(1)

    # potvrzeni pripojeni
    conn, addr = s.accept()

    logging.info('Startuji server')

    return conn

# update a drzeni zprav v chatu
def chat_update(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)
    # pridavani zprav
    if state==0:
        chatlog.insert(END, 'VY: ' + msg)
    else:
        chatlog.insert(END, 'Typek: ' + msg)
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
    conn.send(msg.encode('ascii'))
    textbox.delete("0.0", END)

# prijeti zpravy
def prijem():
    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                chat_update(msg, 1)
        except:
            pass

#definovani pro moznost pouziti tlacitka enter
def enter(event):
    odeslat()

# grafika okna
def GUI():
    global chatlog
    global textbox

    # nastaveni okna
    gui = Tk()
    gui.title("Lide.cz - Server Chat")
    gui.geometry("380x430")

    # zobrazeni textu
    chatlog = Text(gui, bg='white')
    chatlog.config(state=DISABLED)

    # tlacitko odeslat
    sendbutton = Button(gui, bg='white', fg='black', text='SEND', command=odeslat())

    # psani zprav
    textbox = Text(gui, bg='white')

    # pozicovani chatu a zprav
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # bind pro pouziti enteru
    textbox.bind("<KeyRelease-Return>", enter())

    # zachytavani zprav
    _thread.start_new_thread(prijem, ())

    # loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    conn = server_start()
    GUI()