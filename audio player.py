import tkinter as tk
import vlc
from tkinter import font, ttk
import math
import os
import random
import time


if os.path.exists("Music") == False:
    os.mkdir("Music")

songs = []
for i in os.listdir("Music"):
    songs.append(f"Music/{i}")

if len(songs) == 0:
    print("No songs found :(")
    exit()

#import sys
#if len(sys.argv) < 2:
    #print("no file specified")
    #exit()

print("Don't close me :(")

song = songs[0]
if len(songs) > 1:
    next_song_in_queue = songs[1]
songs_original = []
for i in songs:
    songs_original.append(i)
player = vlc.MediaPlayer(song)
player.play()
current_playback_mode = "normal"
previous_playback_mode = "normal"
last_song = songs[len(songs)-1]

def key_press(event):
    key = event.keysym
    match(key):
        case "space":
            play_pause()
        case "Up":
            volume_up(5)
        case "Down":
            volume_down(5)
        case "Right":
            forward(10000)
        case "Left":
            reverse(10000)
        case "Escape":
            root.destroy()
        case _:
            pass

def play_pause():
    if player.get_state() == vlc.State.Playing:
        player.pause()
    else:
        player.play()

def volume_up(amount):
    if player.audio_get_volume() + amount <= 200:
        player.audio_set_volume(player.audio_get_volume()+amount)
    else:
        player.audio_set_volume(200)
    time.sleep(0.05)
    volume_label.config(text=f"Volume: {str(player.audio_get_volume())}")

def volume_down(amount):
    if player.audio_get_volume() - amount >= 0:
        player.audio_set_volume(player.audio_get_volume()-amount)
    else:
        player.audio_set_volume(0)
    time.sleep(0.05)
    volume_label.config(text=f"Volume: {str(player.audio_get_volume())}")

def forward(amount):
    if player.get_time()+amount > player.get_length():
        player.set_time(player.get_length())
    else:
        player.set_time(player.get_time()+amount)

def reverse(amount):
    if player.get_time()-amount < 0:
        player.set_time(0)
    else:
        player.set_time(player.get_time()-amount)

def playback_mode(mode):
    global current_playback_mode
    global next_song_in_queue
    global previous_playback_mode
    global songs
    if current_playback_mode != mode:
        previous_playback_mode = current_playback_mode
        current_playback_mode = mode
        match mode:
            case "normal":
                if previous_playback_mode == "shuffle" and len(songs) > 1:
                    print(songs_original)
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
                    songs = []
                    for i in songs_original:
                        songs.append(i)
                    song_index = songs.index(song)
                    for i in range(song_index):
                        songs.append(songs[0])
                        songs.pop(0)
                    next_song_in_queue = songs[1]
                print(songs)
                loop.config(foreground="black")
                shuffle.config(foreground="black")
                normal.config(foreground="crimson")
            case "shuffle":
                print(songs_original)
                loop.config(foreground="black")
                shuffle.config(foreground="crimson")
                normal.config(foreground="black")
                random.shuffle(songs)
                songs.pop(songs.index(song))
                songs = [song] + songs
                if len(songs) > 1:
                    next_song_in_queue = songs[1]
                else:
                    next_song_in_queue = song
                print(songs)
            case "loop":
                loop.config(foreground="crimson")
                shuffle.config(foreground="black")
                normal.config(foreground="black")

def song_control(direction):
    global player
    global next_song_in_queue
    global songs
    global song
    global last_song
    match direction:
        case "next":
            if current_playback_mode == "loop":
                player.set_time(0)
            else:
                if len(songs) > 1:
                    player.stop()
                    media = vlc.Media(next_song_in_queue)
                    player.set_media(media)
                    player.play()
                    song_index = songs.index(song)
                    for i in range(song_index+1):
                        songs.append(songs[0])
                        songs.pop(0)
                    last_song = song
                    song = next_song_in_queue
                    next_song_in_queue = songs[1]
                else:
                    player.set_time(0)

        case "previous":
            if current_playback_mode == "loop":
                player.set_time(0)
            else:
                if len(songs) < 2:
                    player.set_time(0)
                else:
                    player.stop()
                    media = vlc.Media(last_song)
                    player.set_media(media)
                    player.play()
                    song = last_song
                    songs = [songs[len(songs)-1]] + songs
                    songs.pop(len(songs)-1)
                    last_song = songs[len(songs)-1]
                    next_song_in_queue = songs[1]

    song_title.config(text=song.split("/")[-1])
    print(songs)

def update_progress():
    global played_songs
    global songs
    global player
    global song
    if player.get_state() == vlc.State.Playing:
        progress["value"] = (player.get_time() / player.get_length()) * 100
        minutes = str(math.floor(player.get_time()/1000/60))
        seconds = str(round(player.get_time()/1000%60))
        if int(seconds) == 60:
            seconds = "00"
            minutes = int(minutes) + 1
            minutes = str(minutes)
        if int(minutes) < 10:
            minutes = "0" + str(minutes)
        if int(seconds) < 10 and seconds != "00":
            seconds = "0" + str(seconds)
        length = player.get_length()
        max_minutes = str(math.floor(length/1000/60))
        max_seconds = str(round(length/1000%60))
        if int(max_minutes) < 10:
	        max_minutes = "0" + str(max_minutes)
        if int(max_seconds) < 10 and max_seconds != "00":
	        max_seconds = "0" + str(max_seconds)
        song_length = f"{max_minutes}:{max_seconds}"
        song_progress.config(text=f"{minutes}:{seconds} / {song_length}")
        #if progress["value"] >= progress["maximum"]:
            #song_control("next")
    elif player.get_state() == vlc.State.Ended:
        song_control("next")
    root.after(1000, update_progress)

root = tk.Tk()
root.title("Audio Player")
root.resizable(False, False)

big_text = tk.font.Font(size=12)

playpause = tk.Button(root, text="Play/Pause", command=play_pause, font=big_text, activeforeground="crimson")

volume_row1 = tk.Frame(root)
volume_row2 = tk.Frame(root)
volumeup1 = tk.Button(volume_row1, text="volume +1", command=lambda: volume_up(1), font=big_text, activeforeground="crimson")
volumeup5 = tk.Button(volume_row1, text="volume +5", command=lambda: volume_up(5), font=big_text, activeforeground="crimson")
volumeup10 = tk.Button(volume_row1, text="volume +10", command=lambda: volume_up(10), font=big_text, activeforeground="crimson")
volumedown1 = tk.Button(volume_row2, text="volume -1", command=lambda: volume_down(1), font=big_text, activeforeground="crimson")
volumedown5 = tk.Button(volume_row2, text="volume -5", command=lambda: volume_down(5), font=big_text, activeforeground="crimson")
volumedown10 = tk.Button(volume_row2, text="volume -10", command=lambda: volume_down(10), font=big_text, activeforeground="crimson")

forward_row = tk.Frame(root)
goforward10 = tk.Button(forward_row, text="10 seconds", command=lambda: forward(10000), font=big_text, activeforeground="crimson")
goforward30 = tk.Button(forward_row, text="30 seconds", command=lambda: forward(30000), font=big_text, activeforeground="crimson")
goforward60 = tk.Button(forward_row, text="60 seconds", command=lambda: forward(60000), font=big_text, activeforeground="crimson")

reverse_row = tk.Frame(root)
gobackward10 = tk.Button(reverse_row, text="10 seconds", command=lambda: reverse(10000), font=big_text, activeforeground="crimson")
gobackward30 = tk.Button(reverse_row, text="30 seconds", command=lambda: reverse(30000), font=big_text, activeforeground="crimson")
gobackward60 = tk.Button(reverse_row, text="60 seconds", command=lambda: reverse(60000), font=big_text, activeforeground="crimson")

options_row1 = tk.Frame(root)
options_row2 = tk.Frame(root)
loop = tk.Button(options_row1, text="Loop", font=big_text, command=lambda: playback_mode("loop"), activeforeground="crimson")
normal = tk.Button(options_row1, text="Normal", font=big_text, command=lambda: playback_mode("normal"), activeforeground="crimson", foreground="crimson")
shuffle = tk.Button(options_row1, text="Shuffle", font=big_text, command=lambda: playback_mode("shuffle"), activeforeground="crimson")
previous_song = tk.Button(options_row2, text="Previous song", command=lambda: song_control("previous"), font=big_text, activeforeground="crimson")
next_song = tk.Button(options_row2, text="     Next song      ", command=lambda: song_control("next"), font=big_text, activeforeground="crimson")

stop = tk.Button(root, text="Exit", command=root.destroy, font=big_text, activeforeground="crimson")

progress = ttk.Progressbar(orient="horizontal", length=100, mode="determinate")
song_progress = tk.Label(root, text="", font=big_text)
song_title = tk.Message(root, text=song.split("/")[-1], font=big_text)
song_title.pack(fill="x")
progress.pack(fill="x", pady=(20, 0))
song_progress.pack(fill="x", pady=(0, 20))
playpause.pack(fill="x")

volume_row1.pack(fill="x")
volume_label = tk.Label(volume_row1, text=f"Volume: {str(player.audio_get_volume())}", font=big_text)
volume_label.pack(side="top", fill="x", expand=True, pady=20)
volumeup1.pack(side="left", fill="x", expand=True)
volumeup5.pack(side="left", fill="x", expand=True)
volumeup10.pack(side="left", fill="x", expand=True)
volume_row2.pack(fill="x")
volumedown1.pack(side="left", fill="x", expand=True)
volumedown5.pack(side="left", fill="x", expand=True)
volumedown10.pack(side="left", fill="x", expand=True)

forward_row.pack(fill="x")
forward_label = tk.Label(forward_row, text="Forward", font=big_text)
forward_label.pack(side="top", fill="x", expand=True, pady=20)
goforward10.pack(side="left", fill="x", expand=True)
goforward30.pack(side="left", fill="x", expand=True)
goforward60.pack(side="left", fill="x", expand=True)

reverse_row.pack(fill="x")
reverse_label = tk.Label(reverse_row, text="Reverse", font=big_text)
reverse_label.pack(side="top", fill="x", expand=True, pady=20)
gobackward10.pack(side="left", fill="x", expand=True)
gobackward30.pack(side="left", fill="x", expand=True)
gobackward60.pack(side="left", fill="x", expand=True)

options_row1.pack(fill="x")
options_label = tk.Label(options_row1, text="Playback controls", font=big_text)
options_label.pack(side="top", fill="x", expand=True, pady=20)
loop.pack(side="left", fill="x", expand=True)
normal.pack(side="left", fill="x", expand=True)
shuffle.pack(side="left", fill="x", expand=True)
options_row2.pack(fill="x")
previous_song.pack(side="left", fill="x", expand=True)
next_song.pack(side="left", fill="x", expand=True)

stop.pack(fill="x", pady=(20, 0))

root.update_idletasks()
song_title.config(width=root.winfo_width())

root.bind("<KeyPress>", key_press)

root.after(100, update_progress)
root.mainloop()
