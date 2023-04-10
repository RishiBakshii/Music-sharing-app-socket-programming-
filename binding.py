from client import *

def hoverme1(e):
    playButton.configure(bg='white')
def overme1(e):
    playButton.config(bg=PRIMARY_BG)

playButton.bind("<Enter>",hoverme1)
playButton.bind("<Leave>",overme1)

