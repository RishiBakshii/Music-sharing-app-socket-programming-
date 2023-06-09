import socket
import threading
from tkinter import *
# from tkinter import tkk
from tkinter import filedialog
from playsound import playsound
import pygame
from pygame import mixer
import os
import time
import ftplib
from ftplib import FTP
import ntpath
from pathlib import Path

SONG_COUNTER=0
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

song_selected=None
listbox=None
infoLabel=None
mixer.init()
PAUSED=False
pause_resume_Button=None
playButton=None
filepathLabel=None

def browse_files():
    global listbox,filePathLabel,SONG_COUNTER,listbox

    try:
        filename=filedialog.askopenfilename()
        
        HOSTNAME='127.0.0.1'
        USERNAME='lftpd'
        PASSWORD='lftpd'

        ftp_server=FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding='utf-8'
        ftp_server.cwd('shared-files')
        fname=ntpath.basename(filename)

        with open(filename,'rb') as file:
            ftp_server.storbinary(f'STOR {fname}',file)
        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(SONG_COUNTER,fname)
        SONG_COUNTER+=1
    
    except FileNotFoundError:
        print('Cancel Button Pressed')

def download():
    global listbox,infoLabel

    song_to_download=listbox.get(ANCHOR)
    infoLabel.configure(text=f'Downloading {song_to_download}')

    HOSTNAME='127.0.0.1'
    USERNAME='lftpd'
    PASSWORD='lftpd'
    home=str(Path.home())
    download_path=home+"/Downloads"

    ftp_server=ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
    ftp_server.encoding='utf-8'
    ftp_server.cwd('shared-files')
    local_filename=os.path.join(download_path,song_to_download)
    file=open(local_filename,'wb')

    ftp_server.retrbinary('RETR '+song_to_download,file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text='Download Complete')
    time.sleep(1)

    if(song_selected!=''):
        infoLabel.configure(text='Now Playing'+song_selected)
    else:
        infoLabel.configure(text='')

def play():
    global song_selected,listbox,infoLabel
    song_selected=listbox.get(ANCHOR)
    if(song_selected!=''):
        mixer.music.load(f'music_files\{song_selected}')
        mixer.music.play()
        infoLabel.configure(text=f'Now playing - {song_selected}')
    else:
        infoLabel.configure(text='Please select a song')

def pause_resume():
    global song_selected,infoLabel,PAUSED,pause_resume_Button

    if PAUSED:
        pause_resume_Button.configure(text='Pause⏯️',width=7)
        mixer.music.unpause()
        PAUSED=False
    else:
        pause_resume_Button.configure(text='Resume⏯️',width=8)
        mixer.music.pause()
        PAUSED=True


def musicWindow():
    global PRIMARY_FONT,SECONDARY_FONT,PRIMARY_BG,SECONDARY_BG,W_HEIGHT,W_HEIGHT,listbox,infoLabel,pause_resume_Button,PAUSED,playButton

    window=Tk()
    window.title("Music Window")
    window.iconbitmap('icon\icon.ico')
    window.resizable(width=False,height=False)
    window.geometry(f"{W_WIDTH}x{W_HEIGHT}")
    window.configure(bg=PRIMARY_BG,)


    selectLabel=Label(window,text='SELECT SONG🍟',bg=PRIMARY_BG,font=PRIMARY_FONT)
    selectLabel.place(anchor=CENTER,relx=.5,y=35)

    listbox=Listbox(window,height=10,width=(int(W_WIDTH)-550),activestyle='dotbox',bg='white',borderwidth=2,font=SECONDARY_FONT)
    listbox.place(anchor=CENTER,relx=.5,rely=.3)

    scrollbar1=Scrollbar(listbox)
    scrollbar1.place(relheight=1,relx=1)
    scrollbar1.config(command=listbox.yview)

    playButton=Button(window,text='Play▶️',bg=SECONDARY_BG,font=('calibri',13),width=8,command=play)
    playButton.place(relx=0.4-0.02,anchor=CENTER,rely=.55)

    pause_resume_Button=Button(window,text='Resume⏯️'if PAUSED==True else 'Pause⏯️',width=8,bg=SECONDARY_BG,font=('calibri',13),command=pause_resume)
    pause_resume_Button.place(relx=0.52-0.02,anchor=CENTER,rely=.55)

    uploadButton=Button(window,text='Upload🔃',bg=SECONDARY_BG,font=('calibri',13),width=8)
    uploadButton.place(relx=0.652-0.02,anchor=CENTER,rely=.55)

    downloadButton=Button(window,text='Download⏬',bg=SECONDARY_BG,font=('calibri',13))
    downloadButton.place(relx=0.5,anchor=CENTER,rely=.65)

    infoLabel=Label(window,fg='blue',text='Select a Song',font=SECONDARY_FONT)
    infoLabel.place(relx=.5,rely=.8,anchor=CENTER)

    # for count,files in enumerate(os.listdir('music_files')):
    #     only_music_files=os.fsdecode(files)
    #     listbox.insert(count,only_music_files)


    # bindings -->
    def hoverme1(e):
        playButton.configure(bg='white')
    def overme1(e):
        playButton.config(bg=PRIMARY_BG)
    def hoverme2(e):
        pause_resume_Button.configure(bg='white')
    def overme2(e):
        pause_resume_Button.config(bg=PRIMARY_BG)
    def hoverme3(e):
        uploadButton.configure(bg='white')
    def overme3(e):
        uploadButton.config(bg=PRIMARY_BG)
    def hoverme4(e):
        downloadButton.configure(bg='white')
    def overme4(e):
        downloadButton.config(bg=PRIMARY_BG)

    playButton.bind("<Enter>",hoverme1)
    playButton.bind("<Leave>",overme1)
    pause_resume_Button.bind("<Enter>",hoverme2)
    pause_resume_Button.bind("<Leave>",overme2)
    uploadButton.bind("<Enter>",hoverme3)
    uploadButton.bind("<Leave>",overme3)
    downloadButton.bind("<Enter>",hoverme4)
    downloadButton.bind("<Leave>",overme4)





    window.mainloop()

def recv_msg():
    global CLIENT
    while True:
        try:
            msg=CLIENT.recv(2048).decode("utf-8")
            if msg:
                print(msg)
        except:
            pass
def setup():
    global CLIENT,IP_ADDRESS,PORT,BUFFER_SIZE

    CLIENT=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    CLIENT.connect((IP_ADDRESS,PORT))
    threading.Thread(target=recv_msg).start()
    musicWindow()

setup()


