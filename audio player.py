import tkinter as tk
import vlc
import sys
from tkinter import font, ttk
import math
import time

if len(sys.argv) < 2:
    print("no file specified")
    exit()

print("Don't close me :(")

song = sys.argv[1]
player = vlc.MediaPlayer(song)
player.play()

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

def update_progress():
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
        song_progress.config(text=f"{minutes}:{seconds} / {song_length}")
        if progress["value"] >= progress["maximum"]:
            root.destroy()
    elif player.get_state() == vlc.State.Ended:
        root.destroy()
    root.after(1000, update_progress)

root = tk.Tk()
root.title(song.split("/")[-1])
root.resizable(False, False)

big_text = tk.font.Font(size=20)

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
stop = tk.Button(root, text="Exit", command=root.destroy, font=big_text, activeforeground="crimson")

progress = ttk.Progressbar(orient="horizontal", length=100, mode="determinate")
song_progress = tk.Label(root, text="", font=big_text)
song_title = tk.Label(root, text=song.split("/")[-1], font=big_text)
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

stop.pack(fill="x", pady=(40, 0))

max_minutes = str(math.floor(player.get_length()/1000/60))
max_seconds = str(round(player.get_length()/1000%60))
if int(max_seconds) == 60:
	seconds = "00"
	max_minutes = int(max_minutes) + 1
	max_minutes = str(max_minutes)
if int(max_minutes) < 10:
	max_minutes = "0" + str(max_minutes)
if int(max_seconds) < 10 and max_seconds != "00":
	max_seconds = "0" + str(max_seconds)
song_length = f"{max_minutes}:{max_seconds}"

root.bind("<KeyPress>", key_press)

root.after(100, update_progress)
root.mainloop()
