import math
import os
import time
import tkinter.font
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import keras
import librosa
import numpy as np
import pygame
import tensorflow as tf

root = Tk()
root.title("MGC")
root.iconbitmap('images/logo.ico')
app_height =550
app_width =500
root.geometry(f'{app_width}x{app_height}+{400}+{100}')
root.resizable(False, False)
root.config(background ="light gray")

pygame.mixer.init()
model = keras.models.load_model("MusicGenre_CNN_79.73.h5")

font = tkinter.font.Font(family="Helvetica", size=25, weight="bold")
headerLabel = Label(root, text="MUSIC" + "\n" + " GENRE CLASSIFIER", font=font, bg="light gray",fg="crimson")
headerLabel.pack(side="top", fill="x", pady=20)

infoFont = tkinter.font.Font(family="Helvetica", size=13)
infoLabel = Label(root, text="Welcome, this application is based on Deep Learning and Tkinter."+"\n"+
                             "It has been created so that you can easily learn"+"\n"+
                             "the genres of music that you do not know.",
                  font=infoFont, bg="light gray")
infoLabel.pack()

class BLabel(object):
    b = "•"
    def __init__(self,master):
        import tkinter as ttk
        self.l = ttk.Label(master)
    def add_option(self,text):
        if self.l.cget("text") == "":
            self.l.config(text=self.b+" "+text)
        else:
            self.l.config(text=self.l.cget("text") +"\n"+ self.b + " "+text)


lbal = BLabel(master=root)
lbal.add_option("Load the song you want to learn which genre is          ")
lbal.add_option('Make sure your audio file extension ends with ".wav" ')
lbal.add_option('It will predict the first song in the below list.                 ')
lbal.add_option('Click the "Learn" button                                                   ')

prediction_label = Label(text="", bg="light gray", fg="purple", font=15 )
prediction_label.pack()
lbal.l.pack()

#Grab time length infos of the song
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000 #get position and divided for get seconds
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time)) #minutes and seconds
    statusBar.config(text=f'Time : {converted_current_time}') #make it int because don't want x.y second just x
    statusBar.after(1000, play_time)

def add_song():
    song = filedialog.askopenfilename(initialdir="audio", title="Choose a song for MGC", filetypes=(("wav files", "*.wav"),))
    song_box.insert(END, song)

def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#play selected song
def play_song():
    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Call the play_time function to get current song length
    play_time()

#Create global pause variable because song isn't paused
global paused
paused = False

def pause_song(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#stop current song
def stop_song():
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)
    #Clear the length status bar
    statusBar.config(text='')

def predict_song():
    audio = song_box.get(ACTIVE)
    print(audio)
    if song_box.get(ACTIVE):
        # Audio files pre-processing
        def process_input(audio_file, track_duration):
            SAMPLE_RATE = 22050
            NUM_MFCC = 13
            N_FTT = 2048
            HOP_LENGTH = 512
            TRACK_DURATION = track_duration  # measured in seconds
            SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION
            NUM_SEGMENTS = 10

            samples_per_segment = int(SAMPLES_PER_TRACK / NUM_SEGMENTS)
            num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / HOP_LENGTH)
            signal, sample_rate = librosa.load(audio_file, sr=SAMPLE_RATE)

            for d in range(10):
                # calculate start and finish sample for current segment
                start = samples_per_segment * d
                finish = start + samples_per_segment

                # extract mfcc
                mfcc = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=NUM_MFCC, n_fft=N_FTT,
                                            hop_length=HOP_LENGTH)
                mfcc = mfcc.T
                return mfcc

    audio_file = process_input(audio, 30)
    genre_dict = {0: "disco", 1: "pop", 2: "classical", 3: "metal", 4: "rock", 5: "blues", 6: "hiphop", 7: "reggae",
                  8: "country", 9: "jazz"}
    X_to_predict = audio_file[np.newaxis, ..., np.newaxis]

    pred = model.predict(X_to_predict)
    pred = np.argmax(pred)
    prediction = genre_dict[int(pred)]
    prediction = prediction.upper()

    return  prediction_label.config(text=f'Predicted Genre is : {prediction}')


loadButton = Button(root, text="LOAD", padx=30, pady=10, borderwidth=2, activebackground="gray", bg="#546879",
                          relief=GROOVE, command=add_song)
loadButton.place(x=60, y=300)
deleteButton = Button(root, text="DELETE", padx=30, pady=10, borderwidth=2, activebackground="gray", bg="#546879",
                          relief=GROOVE, command=delete_song)
deleteButton.place(x=190, y=300)
predictButton = Button(root, text="PREDICT", padx=30, pady=10, borderwidth=2, activebackground="gray", bg="#546879",
                          relief=GROOVE, command=predict_song)
predictButton.place(x=320, y=300)

#creatre playlist box
song_box = Listbox(root, bg="black",fg="white",height=5, width=62,
                   selectbackground="#1167b1", selectforeground="white")
song_box.place(x=60 ,y=360)

#Define control buttons images
playButtonImage = PhotoImage(file="images/start.png")
pauseButtonImage = PhotoImage(file="images/pause.png")
stopButtonImage = PhotoImage(file="images/stop.png")

#Create player control frame
controlsFrame = Frame(root)
controlsFrame.place(x=135, y=460)

#create player control button
playButton = Button(controlsFrame, image=playButtonImage, borderwidth=0, command=play_song)
pauseButton = Button(controlsFrame, image=pauseButtonImage, borderwidth=0, command=lambda: pause_song(paused))
stopButton = Button(controlsFrame, image=stopButtonImage, borderwidth=0, command=stop_song)

pauseButton.grid(row=0, column=1, padx=10)
playButton.grid(row=0, column=2, padx=10)
stopButton.grid(row=0, column=3, padx=10)

#Create status bar
statusBar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=2)

root.mainloop()