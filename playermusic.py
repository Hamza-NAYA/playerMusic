# Importation des bibliothèques nécessaires
from pygame import mixer
from tkinter import ttk
import tkinter as tk
import customtkinter as ctk
import random
import os
import fnmatch
# Utilisation de la bibliothèque customtkinter 
# pour styliser le format traditionnel de l'interphace graphique fourni par tkinter
# pour installer cette bibliothèque : pip install customtkinter


# Configuration de l'apparence de la fenêtre
ctk.set_appearance_mode("dark")

# Initialisation de la fenêtre principale
fenetre = ctk.CTk()
fenetre.title("PlayerMusic")
fenetre.geometry("800x550")
fenetre.config(bg="white")

# Creation des variables pour l'emplacement du dossier music et pour reconnaitre une fichier music
rootpath = "music"
pattern = "*.mp3"

# Initialisation de Pygame pour la gestion de la musique
mixer.init()

# Chargement des images des boutons
prec_img = tk.PhotoImage(file="images/prev.png")
stop_img = tk.PhotoImage(file="images/stop.png")
play_img = tk.PhotoImage(file="images/play.png")
pause_img = tk.PhotoImage(file="images/pause.png")
suivant_img = tk.PhotoImage(file="images/next.png")
random_img = tk.PhotoImage(file="images/random.png")

# Fonction pour sélectionner une chanson dans la liste
def select():
    selected_song = listBox.get("anchor")
    label.config(text=selected_song)

    mixer.music.load(os.path.join(rootpath, selected_song))
    mixer.music.play()

    progress.config(value=0, maximum=mixer.Sound(os.path.join(rootpath, selected_song)).get_length())

# Fonction pour arrêter la lecture de la musique
def stop():
    mixer.music.stop()
    listBox.select_clear("active")

# Fonction pour passer à la chanson suivante
def suivant():
    next_song = listBox.curselection()
    next_song = next_song[0]+1
    next_song_name = listBox.get(next_song)

    label.config(text= next_song_name)
    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()

    listBox.select_clear(0, "end")
    listBox.activate(next_song)
    listBox.select_set(next_song)

# Fonction pour revenir à la chanson précédente
def prec():
    prec_song = listBox.curselection()
    prec_song = prec_song[0]-1
    prec_song_name = listBox.get(prec_song)

    label.config(text= prec_song_name)
    mixer.music.load(rootpath + "\\" + prec_song_name)
    mixer.music.play()

    listBox.select_clear(0, "end")
    listBox.activate(prec_song)
    listBox.select_set(prec_song)

# Fonction pour mettre en pause ou reprendre la lecture de la musique
def pause():
    if pauseButtton["text"] == "pause":
        mixer.music.pause()
        pauseButtton["text"] = "play"
    else:
        mixer.music.unpause()
        pauseButtton["text"] = "pause"

# Fonction pour jouer une chanson au hasard
def random_song():
    listBox.select_clear(0, "end")
    random_index = random.randint(0, listBox.size()-1)
    random_song_name = listBox.get(random_index)

    label.config(text=random_song_name)
    mixer.music.load(os.path.join(rootpath, random_song_name))
    mixer.music.play()

    listBox.activate(random_index)
    listBox.select_set(random_index)

# Fonction pour mettre à jour la barre de progression
def update_progress():
    current_time = mixer.music.get_pos() / 1000
    progress.config(value=current_time)
    fenetre.after(1000, update_progress)

# Liste des chansons dans le répertoire spécifié
listBox= tk.Listbox(fenetre, fg="grey", bg="black", width=100,font=("bahnschrift", 14))
listBox.pack(padx=20, pady=20)

# Label pour afficher le nom de la chanson sélectionnée
label = tk.Label(fenetre , text="", bg="white" , fg="grey", font=("bahnschrift", 16))
label.pack(pady=15)

# Cadre pour les boutons de contrôle
top = tk.Frame(fenetre, bg="white")
top.pack(padx=10, pady=5, anchor="center")

# Boutons de contrôle
precButtton = tk.Button(fenetre, text="prec", image=prec_img, bg="white", borderwidth=0, command=prec)
precButtton.pack(pady=15, in_=top, side="left")

stopButtton = tk.Button(fenetre, text="stop", image=stop_img, bg="white", borderwidth=0, command=stop)
stopButtton.pack(pady=15, in_=top, side="left")

playButtton = tk.Button(fenetre, text="play", image=play_img, bg="white", borderwidth=0, command=select)
playButtton.pack(pady=15, in_=top, side="left")

pauseButtton = tk.Button(fenetre, text="pause", image=pause_img, bg="white", borderwidth=0, command=pause)
pauseButtton.pack(pady=15, in_=top, side="left")

suivantButtton = tk.Button(fenetre, text="suivant", image=suivant_img, bg="white", borderwidth=0, command=suivant)
suivantButtton.pack(pady=15, in_=top, side="left")

random_button = tk.Button(fenetre, text="aléatoire", image=random_img, bg="white", borderwidth=0, command=random_song)
random_button.pack(pady=15, in_=top, side="left")

# Configuration du style de la barre de progression
s = ttk.Style()
s.theme_use("alt")
s.layout("progressbar",[('Horizontal.Progressbar.trough',{'children': [('Horizontal.Progressbar.pbar',{'side': 'left', 'sticky': 'ns'})],'sticky': 'nswe'})])

s.configure("progressbar", troughcolor="grey", background="black", thickness=1)

# Contrôle du volume
volume_scale = ttk.Scale(fenetre, from_=0, to=100, length=300, orient="horizontal", command=lambda x: mixer.music.set_volume(float(x) / 100))
volume_scale.set(50)
volume_scale.pack(pady=10)

# Barre de progression
progress = ttk.Progressbar(fenetre, length=750, mode="determinate", style="progressbar")
progress.pack(pady=10)

# Remplissage de la liste des chansons
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files,pattern):
        listBox.insert("end", filename)

# Mise à jour continue de la barre de progression
update_progress()

# Lancement de la boucle principale de la fenêtre
fenetre.mainloop()