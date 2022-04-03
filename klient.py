#importy
import socket
from tkinter import *
from socket import *
import _thread

# nastaveni spojeni klienta se serverem
def klient_start():
    # nastaveni sockeru
    s = socket(AF_INET, SOCK_STREAM)

    # detaily
    host = gethostname()
    port = 2222

    # pripojeni
    try:
        s.connect((host, port))
    except Exception as CRE:
        print("Error while connectiong to server:")
        print(CRE)

    return s


# update a drzeni zprav v chatu
def chat_update(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)
    # pridavani zprav
    if state == 0:
        chatlog.insert(END, ' VY: ' + msg)
    else:
        chatlog.insert(END, ' THOTKA: ' + msg)
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
    s.send(msg.encode('utf8'))
    textbox.delete("0.0", END)


# prijeti zpravy
def prijem():
    while 1:
        try:
            data = s.recv(1024)
            msg = data.decode('UTF-8')
            if msg != "":
                chat_update(msg, 1)
        except:
            pass

#definovani pro moznost pouziti tlacitka enter
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
    textbox.bind("<KeyRelease-Return>", press)

    # zachytavani zprav
    _thread.start_new_thread(prijem, ())

    # loop
    gui.mainloop()

#konec
if __name__ == '__main__':
    chatlog = textbox = None
    s = klient_start()
    GUI()
else:
    print("--> Connection failed")