from math import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
from resizeimage import resizeimage
import PIL
import ctypes
import random
import ntpath
import os

#fenetre
user32 = ctypes.windll.user32 #recup info
screenw, screenh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) #recup resolution de l'ecran
windoww, windowh = int(screenw/2), int(screenh/2) #resolution ecran/2
window = Tk() #crée fenetre
window.title('Project "tew"') #titre
window.geometry('%sx%s' % (windoww, windowh)) #taille de fenetre = resolution ecran/2
window.resizable(width = False, height = False) #verrouille taille de la fenetre
window.iconbitmap("icon.ico") #logo

#fonctions
def about() : #fenetre a propos
    messagebox.showinfo("À propos", "Ce programme a été crée dans le cadre de l'épreuve\nde BAC d'ISN.\n\nCrée par :\n-Valentin Bernard\n-Antoine Qiu")

def help() : #fenetre aide
    messagebox.showinfo("Aide ?", "Mode d'emploi :\n-Sélectionnez une image en cliquant sur Parcourir...\n-Le mode Générer une image clé permet de chiffrer une image sans avoir une image clé à disposition. A noter que le chiffrement peut être un peu plus long.\n-Le mode Utiliser une image clé existante nécessite une image clé. Celui-ci permet de chiffrer et de dechiffrer une image. A noter que l'image clé doit être au moins aussi grande que l'image originale.\n\nNote :\n-Une image qui a été chiffrée ne peut être déchiffrée uniquement avec l'image clé qui a servi à la chiffrer.\n-Les fichiers de sorties (image (dé)chiffrée et clé) sont trouvable au même endroit que le programme.\n-Plus l'image est grande, plus le processus prend du temps.")

def browse() : #selection image a (dé)chiffrer
    file = filedialog.askopenfilename(initialdir = "/",title = "Veuillez choisir une image",filetypes = (("Image","*.jpg"),("Image","*.png"),("Image","*.jpeg"))) #ouvre fenetre pour selec img
    if file == "" :
        path.configure(text = "...") #modif affichage
    else :
        path.configure(text = file) #affiche chemin sur dans interface
    
def form(list) : #converti en liste de 8 termes
    while len(list) < int("8") :
        list.insert(0, "0")
    return(list)

def add(img,key) : #addition de l'image et de la clé par la fonction XOR
    c = [0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    while int(i) < int("8") :
        if int(img[i]) + int(key[i]) == int("0") :
            c[i] = 0
        if int(img[i]) + int(key[i]) == int("1") :
            c[i] = 1
        if int(img[i]) + int(key[i]) == int("2") :
            c[i] = 0
        i = i+1
    return(c)

def crypt() : #fonction (dé)chiffrer image avec clé existante
    if path.cget("text") == "..." : #verif si img selectionné
        messagebox.showerror("Erreur", "Aucune image selectionée.\nVeuillez réessayer.")
    else :
        img = Image.open(path.cget("text")) #recup chemin
        key = Image.open(filedialog.askopenfilename(initialdir = "/",title = "Veuillez choisir une image clé",filetypes = (("Image","*.jpg"),("Image","*.png"),("Image","*.jpeg"))))
        if key.size[0] < img.size[0] or key.size[1] < img.size[1] : #image doit être <ou= à la clé
            messagebox.showerror("Erreur", "L'image clé selectionnée est trop petite.\nVeuillez réessayer avec une image clé de taille supérieure ou égale à celle de l'image à chiffrer.")
        else :
            messagebox.showwarning("Attention !", "Il se peut que le programme fige pendant le processus de chiffrement.\nVeuillez patienter jusqu'à ce que le programme réponde.\nVeuillez appuyer sur OK pour commencer le chiffrement.")
            size = [img.size[0], img.size[1]] #recup taille de l'image
            key = resizeimage.resize_cover(key, size) #taille clé = taille image
            if img.mode == "P" : #force image en rgb
                img = img.convert("RGB")
            if key.mode == "P" :
                key = key.convert("RGB")
            pixelimg = img.load() #charge les pixels
            pixelkey = key.load()
            if img.mode == "RGBA" : #rgba prend en compte transparence contrairement au rgb
                for x in range(img.size[0]):    # for every col
                    for y in range(img.size[1]):    # For every row
                        rimg, gimg, bimg, timg = pixelimg[x, y] #stock chaque pixel dans variable red green blue transparent
                        rimg, gimg, bimg = form(list(bin(rimg)[2:])), form(list(bin(gimg)[2:])), form(list(bin(bimg)[2:])) #serie de manipulation et convertions
                        if key.mode == "RGBA" :
                            rkey, gkey, bkey, tkey = pixelkey[x, y]
                            rkey, gkey, bkey = form(list(bin(rkey)[2:])), form(list(bin(gkey)[2:])), form(list(bin(bkey)[2:]))      
                        else :
                            rkey, gkey, bkey = pixelkey[x, y]
                            rkey, gkey, bkey = form(list(bin(rkey)[2:])), form(list(bin(gkey)[2:])), form(list(bin(bkey)[2:]))
                        rimg, gimg, bimg = add(rimg, rkey), add(gimg, gkey), add(bimg, bkey) #addition XOR
                        rimg, gimg, bimg = "".join(str(e) for e in rimg), "".join(str(e) for e in gimg), "".join(str(e) for e in bimg) #supprime les espaces
                        rimg, gimg, bimg = int(rimg, 2), int(gimg, 2), int(bimg, 2) #converti en valeur rgb
                        pixelimg[x,y] = (rimg, gimg, bimg, timg) #ecrase les pixels de l'image
            else :
                for x in range(img.size[0]):    # for every col:
                    for y in range(img.size[1]):    # For every row
                        rimg, gimg, bimg = pixelimg[x, y]
                        rimg, gimg, bimg = form(list(bin(rimg)[2:])), form(list(bin(gimg)[2:])), form(list(bin(bimg)[2:]))
                        if key.mode == "RGBA" :
                            rkey, gkey, bkey, tkey = pixelkey[x, y]
                            rkey, gkey, bkey = form(list(bin(rkey)[2:])), form(list(bin(gkey)[2:])), form(list(bin(bkey)[2:]))      
                        else :
                            rkey, gkey, bkey = pixelkey[x, y]
                            rkey, gkey, bkey = form(list(bin(rkey)[2:])), form(list(bin(gkey)[2:])), form(list(bin(bkey)[2:]))
                        rimg, gimg, bimg = add(rimg, rkey), add(gimg, gkey), add(bimg, bkey)
                        rimg, gimg, bimg = "".join(str(e) for e in rimg), "".join(str(e) for e in gimg), "".join(str(e) for e in bimg)
                        rimg, gimg, bimg = int(rimg, 2), int(gimg, 2), int(bimg, 2)
                        pixelimg[x,y] = (rimg, gimg, bimg)
            imgname = ntpath.basename(path.cget("text")) #recup nom img
            imgname = imgname.replace(".png", "") #supprime extension du nom
            imgname = imgname.replace(".PNG", "")
            imgname = imgname.replace(".jpg", "")
            imgname = imgname.replace(".JPG", "")
            imgname = imgname.replace(".jpeg", "")
            imgname = imgname.replace(".JPEG", "")
            imgcryptname = [imgname,"-(Un)crypted.png"] #ajout suffixe dans le nom
            imgcryptname = "".join(str(e) for e in imgcryptname) #supprime les espaces
            img.save(imgcryptname, "png") #sauvegarde image
            path.configure(text = "...")
            messagebox.showinfo("Succès !", "Le (dé)chiffrement s'est déroulé avec succès !\nVeuillez retrouver les images (dé)chiffrés dans le dossier du programme.")
        
def cryptrandom() : #fonction (dé)chiffre image avec génération de clé
    if path.cget("text") == "..." : #verif si img selectionné
        messagebox.showerror("Erreur", "Aucune image selectionée.\nVeuillez réessayer.")
    else :
        messagebox.showwarning("Attention !", "Il se peut que le programme fige pendant le processus de chiffrement.\nVeuillez patienter jusqu'à ce que le programme réponde.\nVeuillez appuyer sur OK pour commencer le chiffrement.")
        img = Image.open(path.cget("text"))
        h, w = img.size[0], img.size[1]
        size = [h, w]
        key = PIL.Image.new("RGB", size) #crée clé même taille que image
        pixel = key.load()
        for x in range(key.size[0]): #pixels aléatoires
            for y in range(key.size[1]):
                r = random.randint(1, 256)
                g = random.randint(1, 256)
                b = random.randint(1, 256)
                pixel[x, y] = (r, g, b)
        imgname = ntpath.basename(path.cget("text")) #nom img
        imgname = imgname.replace(".png", "")
        imgname = imgname.replace(".PNG", "")
        imgname = imgname.replace(".jpg", "")
        imgname = imgname.replace(".JPG", "")
        imgname = imgname.replace(".jpeg", "")
        imgname = imgname.replace(".JPEG", "")
        keyname = [imgname,"-Key.png"]
        keyname = "".join(str(e) for e in keyname)
        key.save(keyname, "png")
        if img.mode == "P" :
            img = img.convert("RGB")
        pixelimg = img.load()
        pixelkey = key.load()
        if img.mode == "RGBA" :
            for x in range(img.size[0]):    # for every col:
                for y in range(img.size[1]):    # For every row
                    rimg, gimg, bimg, timg = pixelimg[x, y]
                    rimg, gimg, bimg = form(list(bin(rimg)[2:])), form(list(bin(gimg)[2:])), form(list(bin(bimg)[2:]))
                    rkey, gkey, bkey = pixelkey[x, y]
                    rkey, gkey, bkey = form(list(bin(rkey)[2:])), form(list(bin(gkey)[2:])), form(list(bin(bkey)[2:]))
                    rimg, gimg, bimg = add(rimg, rkey), add(gimg, gkey), add(bimg, bkey)
                    rimg, gimg, bimg = "".join(str(e) for e in rimg), "".join(str(e) for e in gimg), "".join(str(e) for e in bimg)
                    rimg, gimg, bimg = int(rimg, 2), int(gimg, 2), int(bimg, 2)
                    pixelimg[x,y] = (rimg, gimg, bimg, timg)
        else :
            for x in range(img.size[0]):    # for every col:
                for y in range(img.size[1]):    # For every row
                    rimg, gimg, bimg = pixelimg[x, y]
                    rimg, gimg, bimg = form(list(bin(rimg)[2:])), form(list(bin(gimg)[2:])), form(list(bin(bimg)[2:]))
                    rkey, gkey, bkey = pixelkey[x, y]
                    rkey, gkey, bkey = form(list(bin(rkey)[2:])), form(list(bin(gkey)[2:])), form(list(bin(bkey)[2:]))
                    rimg, gimg, bimg = add(rimg, rkey), add(gimg, gkey), add(bimg, bkey)
                    rimg, gimg, bimg = "".join(str(e) for e in rimg), "".join(str(e) for e in gimg), "".join(str(e) for e in bimg)
                    rimg, gimg, bimg = int(rimg, 2), int(gimg, 2), int(bimg, 2)
                    pixelimg[x,y] = (rimg, gimg, bimg)
        imgcryptname = [imgname,"-Crypted.png"]
        imgcryptname = "".join(str(e) for e in imgcryptname)
        img.save(imgcryptname, "png")
        path.configure(text = "...")
        messagebox.showinfo("Succès !", "Le chiffrement s'est déroulé avec succès !\nVeuillez retrouver les images (dé)chiffrés dans le dossier du programme.")

def error() : #message d'erreur si aucune selection
    messagebox.showerror("Erreur", "Aucune méthode selectionée.\nVeuillez réessayer.")
        
def sel() : #change boutton selon selection
    if str(var.get()) == "1" : 
        btncrypt.configure(command = cryptrandom)
    if str(var.get()) == "2" : 
        btncrypt.configure(command = crypt)

#interface
file = ""
Label(window, text = "Ce programme est capable de (dé)chiffrer une image par la fonction XOR.").grid(row = 0)
casePath = Label(window, text = "")
casePath.grid(row = 3)
Label(casePath, text = "\nVeuillez choisir une image :").grid()
path = Label(casePath, text = "...")
path.grid(row = 1)
btnpath = Button(window, text = "Parcourir...", command = browse)
btnpath.grid(row = 5)
Label(window, text = "\n\nVeuillez choisir une méthode :").grid(row = 7)
caseRadio = Label(window, text = "")
caseRadio.grid(row = 8)
var = IntVar()
Radiobutton(caseRadio, text = "Générer une image clé (Uniquement pour chiffrer)", variable = var, value = 1, command = sel).grid(column = 0, row = 0)
Radiobutton(caseRadio, text = "Utiliser une image clé existante (Chiffrer ou déchiffrer)", variable = var, value = 2, command = sel).grid(column = 0, row = 1)
btncrypt = Button(window, text = "Chiffrer/Déchiffrer", command = error)
btncrypt.grid(row = 11)
Label(window).grid(row = 10) #espaces pour arranger
Label(window).grid(row = 12)
Label(window).grid(row = 13)
Label(window).grid(row = 14)
Label(window).grid(row = 15)
Label(window).grid(row = 17)
caseAbout = Label(window)
caseAbout.grid(row = 16)
Button(caseAbout, text = "À propos", width = 7, command = about).grid(column = 0, row = 0)
Label(caseAbout).grid(column = 1, row = 0)
Button(caseAbout, text = "Aide ?", width = 7, command = help).grid(column = 2, row = 0)
ttk.Progressbar(window, orient = "horizontal",length = screenw/2).grid(row = 18) #barre de progression servant uniquement a centre les widgets car on utilise grid

window.mainloop()
