from tkinter import messagebox
from tkinter import *
import ctypes
import subprocess

#fenetre
user32 = ctypes.windll.user32 #recup info
screenw, screenh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) #recup resol ecran
windoww, windowh = int(screenw/4), int(screenh/4) #resolution ecran/4
window = Tk() #crée fenetre
window.title('Project "tew"') #titre
window.geometry('%sx%s' % (windoww, windowh)) #taille de fenetre = resolution ecran/4
window.resizable(width = False, height = False) #verrouille taille de la fenetre
window.iconbitmap("icon.ico") #logo

#fonctions
def about() : #fenetre a propos
    messagebox.showinfo("À propos", "Ce programme a été crée dans le cadre de l'épreuve\nde BAC d'ISN.\n\nCrée par :\n-Valentin Bernard\n-Antoine Qiu")

def mode1() : #chiffrement 1
    window.withdraw()
    subprocess.run("Mode1.pyw", shell = True)
    exit()

def mode2() : #chiffrement 2
    window.withdraw()
    subprocess.Popen("Mode2.pyw", shell = True)
    exit()

#interface
Label(window, text = "\nBienvenue dans notre programme de chiffrement.\n\nVous pouvez choisr une des deux methodes\nde chiffrement ci-dessous.\n\n").pack()
caseBouton = Label(window)
caseBouton.pack()
Button(caseBouton, text = "Aléatoire", width = 10, command = mode1).grid(column = 0, row = 0)
Label(caseBouton, text = "                    ").grid(column = 1, row = 0)
Button(caseBouton, text = "XOR", width = 10, command = mode2).grid(column = 2, row = 0)
Label(window).pack()
Button(window, text = "À propos", command = about).pack()

window.mainloop()

