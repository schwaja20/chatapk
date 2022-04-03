#importy
import socket
from tkinter import *
from socket import *
import _thread
import logging

#logging config
logging.basicConfig(
    filename='server_log.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s : %(message)s',
    datefmt='[%d/%m/%Y] %H:%M:%S'
)


# nastaveni spojeni se serverem
def server_start():

    logging.info('--> starting server')
    # nastaveni sockeru
    serversocket = socket(AF_INET, SOCK_STREAM)

    # detaily
    host = gethostname()
    port = 2222

    # pripojeni serveru
    try:
        serversocket.bind((host, port))
    except Exception as e:
        print(" ")
        print("Error while starting a server:")
        print(e)
        print(" ")

        logging.error(e)

    serversocket.listen()
    print("Server listening on port", port)
    logging.info("Server is listening...")

    # potvrzeni pripojeni a zalogovani udalosti
    conn, addr = serversocket.accept()

    print("Connection established with", addr)
    logging.info("Connection established with " + str(addr))

    return conn

clients = set()

# update a drzeni zprav v chatu
def chat_update(msg, state):
    global chatlog

    for client in clients:
        try:
            client.send(msg.encode('utf-8'))
        except Exception as Ex:
            print(" ")
            print("Error while sending a message:")
            print(Ex)
            print(" ")

            logging.error(Ex)

    chatlog.config(state=NORMAL)
    # pridavani zprav
    if state==0:
        chatlog.insert(END, ' VY: ' + msg)
    else:
        chatlog.insert(END, ' Typek: ' + msg)
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
    while True:
        try:
            data = conn.recv(1024)
            msg = data.decode('utf8')
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
    gui.configure(bg="black", highlightthickness=1)

    # zobrazeni textu
    chatlog = Text(gui, bg='black', fg="#5AC700", highlightthickness=1)
    chatlog.config(state=DISABLED)

    # tlacitko odeslat
    sendbutton = Button(gui, bg='white', fg='black', text='SEND', command=odeslat, highlightthickness=1)

    # psani zprav
    textbox = Text(gui, bg='black', fg="#5AC700", highlightthickness=1)

    # pozicovani chatu a zprav
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # bind pro pouziti enteru
    textbox.bind("<KeyRelease-Return>", enter)

    # zachytavani zprav
    try:
        _thread.start_new_thread(prijem, ())
        logging.info("--> Klient connected")
    except Exception as Ex:
        print(" ")
        print("An error has occurred")
        print(Ex)
        print(" ")

        logging.error(Ex)

    # loop
    gui.mainloop()


if __name__ == '__main__':
    chatlog = textbox = None
    conn = server_start()
    logging.info("--> server start OK")
    GUI()
else:
    print("--> Connection failed")
    logging.info("--> Connection failed")