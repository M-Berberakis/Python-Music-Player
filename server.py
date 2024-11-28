import sqlite3
import hashlib
import socket
import threading 
import tkinter as tk
import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer

musicFilesIndex = 0

myAudioServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myAudioServer.bind(("localhost", 5050))

print("Connection to localhost was successful...")
myAudioServer.listen()

def windowPlayerCreation():
    frame = tk.Tk()
    frame.title("Music Media Player")
    frame.geometry("900x1000")
    frame.config(bg='#bad19b')

    mixer.init()

    usermusicFiles = []

    def getmusicFiles():
        musicFiles = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3;*.wav")])
        for musicFiles in musicFiles:
            usermusicFiles.append(musicFiles)

            musicFileName = os.path.basename(musicFiles)

            musicList.insert('end', musicFileName)

    def playMusic():
        global musicFilesIndex
        if usermusicFiles:
            musicFiles = usermusicFiles[musicFilesIndex]
            print(f"Playing: {musicFiles}")

            mixer.music.load(musicFiles)
            mixer.music.play()

            musicList.select_clear(0, tk.END)
            musicList.select_set(musicFilesIndex)

            musicList.itemconfig(musicFilesIndex, {'bg': '#94c8e3'})

    def stopMusic():
        mixer.music.stop()
        musicList.select_clear("active")

    def musicNext():
        global musicFilesIndex
        if usermusicFiles:
            musicFilesIndex = (musicFilesIndex + 1) % len(usermusicFiles)
            playMusic()

    def musicPrev():
        global musicFilesIndex
        if usermusicFiles:
            musicFilesIndex = (musicFilesIndex - 1) % len(usermusicFiles)
            playMusic()

    def setVolume(val):
        volume = int(val) / 100.0
        mixer.music.set_volume(volume)

    musicList = tk.Listbox(frame, fg="black", bg="white", width=30, font=("Arial", 20))
    musicList.pack(padx=5, pady=5)

    # Automatically load audio files from the "AudioFiles" folder
    audio_files_folder = "AudioFiles"
    for file in os.listdir(audio_files_folder):
        if file.endswith(".mp3") or file.endswith(".wav"):
            usermusicFiles.append(os.path.join(audio_files_folder, file))
            musicFileName = os.path.basename(file)
            musicList.insert('end', musicFileName)

    top = tk.Frame(frame)
    top.pack(padx=5, pady=5, anchor="center")

    musicTitle = tk.Label(frame, text='', font="Arial")
    musicTitle.pack(pady=5, in_=top, side='top')

    browseAudioFiles = tk.Button(frame, text="Browse", command=getmusicFiles, width=15, height=2, font=("Arial", 14), highlightbackground='#bad19b', highlightcolor='#bad19b')
    browseAudioFiles.pack(pady=10, in_=top, side="top")

    musicPrevBtn = tk.Button(frame, text="Prev", command=musicPrev, width=15, height=2, font=("Arial", 14), highlightbackground='#bad19b', highlightcolor='#bad19b')
    musicPrevBtn.pack(pady=10, in_=top, side="top")

    stopMusicBtn = tk.Button(frame, text="Pause", command=stopMusic, width=15, height=2, font=("Arial", 14), highlightbackground='#bad19b', highlightcolor='#bad19b')
    stopMusicBtn.pack(pady=10, in_=top, side="top")

    playMusicBtn = tk.Button(frame, text="Play", command=playMusic, width=15, height=2, font=("Arial", 14), highlightbackground='#bad19b', highlightcolor='#bad19b')
    playMusicBtn.pack(pady=10, in_=top, side="top")

    musicNextBtn = tk.Button(frame, text="Next",  command=musicNext, width=15, height=2, font=("Arial", 14), highlightbackground='#bad19b', highlightcolor='#bad19b')
    musicNextBtn.pack(pady=10, in_=top, side="top")

    volumeLabel = tk.Label(frame, text="Volume", font=("Arial", 14))
    volumeLabel.pack(pady=5, in_=top, side="top")

    volumeControl = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, command=setVolume, font=("Arial", 12))
    volumeControl.set(50)  # Set the initial volume to 50%
    volumeControl.pack(pady=5, in_=top, side="top")

    frame.mainloop()

numOfClients = 0
def userAuthentication(clientConnected):
    global numOfClients 
    numOfClients += 1 

    while True:
        userInput = clientConnected.recv(1024).decode()

        if userInput == "R":   
            userLog = clientConnected.recv(1024).decode()
            userPass = clientConnected.recv(1024).decode()

            passEncryption = hashlib.sha256(userPass.encode()).hexdigest()

            databseConnection = sqlite3.connect("userInformation.db")
            databaseCursor = databseConnection.cursor()

            databaseCursor.execute("INSERT INTO userInformation (userLog, userPass) VALUES (?, ?)", (userLog, passEncryption))

            databseConnection.commit()

            databseConnection.close()

            clientConnected.send("You have registered successfully".encode())

        elif userInput == "S": 

            userLog = clientConnected.recv(1024).decode()
            userPass = clientConnected.recv(1024).decode()

            print(f"Retrieved: userLog: {userLog}, userPass: {userPass}")

            passEncryption = hashlib.sha256(userPass.encode()).hexdigest()
            print(f"Encrypted userPass: {passEncryption}")

            databseConnection = sqlite3.connect("userInformation.db")
            databaseCursor = databseConnection.cursor()

            databaseCursor.execute("SELECT * FROM userInformation WHERE userLog=? AND userPass=?", (userLog, passEncryption))
            userCredentials = databaseCursor.fetchone()

            databseConnection.close()

            if userCredentials:
                clientConnected.send("You're signed in".encode())

                windowPlayerCreation()
                break  
            else:
                clientConnected.send("Login was unsuccessful, please enter the correct username and password".encode())

                break

        elif userInput == "Q":
            break

while True:
    myAudioClient, clientAddr = myAudioServer.accept()

    threading.Thread(target=userAuthentication, args=(myAudioClient,)).start()

    print(f"Client connections: {numOfClients}")
