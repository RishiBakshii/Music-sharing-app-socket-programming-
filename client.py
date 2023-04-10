import socket
import threading
from tkinter import *
# from tkinter import tkk
from tkinter import filedialog

IP_ADDRESS='127.0.0.1'
PORT=8050
CLIENT=None
BUFFER_SIZE=4096
PRIMARY_FONT=('calibri',17)
SECONDARY_FONT=('calibri',14)
PRIMARY_BG='LightSkyBlue'
SECONDARY_BG='SkyBlue'
W_WIDTH=600
W_HEIGHT=600


def musicWindow():
    global PRIMARY_FONT,SECONDARY_FONT,PRIMARY_BG,SECONDARY_BG,W_HEIGHT,W_HEIGHT

    window=Tk()
    window.title("Music Window")
    window.geometry(f"{W_WIDTH}x{W_HEIGHT}")
    window.configure(bg=PRIMARY_BG)


    selectLabel=Label(window,text='SELECT SONG🍟',bg=PRIMARY_BG,font=PRIMARY_FONT)
    selectLabel.place(anchor=CENTER,relx=.5,y=35)

    listbox=Listbox(window,height=10,width=(int(W_WIDTH)-520),activestyle='dotbox',bg='white',borderwidth=2,font=SECONDARY_FONT)
    listbox.place(anchor=CENTER,relx=.5,rely=.3)

    scrollbar1=Scrollbar(listbox)
    scrollbar1.place(relheight=1,relx=1)
    scrollbar1.config(command=listbox.yview)

    playButton=Button(window,text='Play▶️',width=7,height=2,bd=1,bg=SECONDARY_BG,font=('calibri',10))
    playButton.place(relx=0.4,anchor=CENTER,rely=.55)

    stopButton=Button(window,text='Stop⏹️',width=7,height=2,bd=1,bg=SECONDARY_BG,font=('calibri',10))
    stopButton.place(relx=0.5,anchor=CENTER,rely=.55)

    uploadButton=Button(window,text='Upload🔃',width=7,height=2,bd=1,bg=SECONDARY_BG,font=('calibri',10))
    uploadButton.place(relx=0.6,anchor=CENTER,rely=.55)

    downloadButton=Button(window,text='Download⏬',width=10,height=2,bd=1,bg=SECONDARY_BG,font=('calibri',10))
    downloadButton.place(relx=0.5,anchor=CENTER,rely=.65)

    infoLabel=Label(window,text='info',fg='blue',font=SECONDARY_FONT)
    infoLabel.place(relx=.5,rely=.8,anchor=CENTER)

    window.mainloop()


def setup():
    global CLIENT,IP_ADDRESS,PORT,BUFFER_SIZE

    CLIENT=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    CLIENT.connect((IP_ADDRESS,PORT))
    musicWindow()

setup()

