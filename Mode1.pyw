import pickle
ouvrir = open
from PIL.Image import *
from random import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
import PIL
from math import *
import ctypes
import os
#fenetre
user32 = ctypes.windll.user32 #recup info
screenw, screenh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) #recup resol ecran
windoww, windowh = int(screenw/2), int(screenh/2) #resolution ecran/2
window = Tk() #crée fenetre
window.title('Project "tew"') #titre
window.geometry('%sx%s' % (windoww, windowh)) #taille de fenetre = taille ecran/2
window.resizable(width = False, height = False) #verrouille taille de la fenetre
window.iconbitmap("icon.ico") #logo

#fonctions
def about() : #fenetre a propos
    messagebox.showinfo("À propos", "Ce programme a été crée dans le cadre de l'épreuve\nde BAC d'ISN.\n\nCrée par :\n-Valentin Bernard\n-Antoine Qiu")

def help() : #fenetre aide
    messagebox.showinfo("Aide ?", "Mode d'emploi :\n-Sélectionnez une image en cliquant sur Parcourir...\n-Si vous souhaitez la chiffrer cliquez simplement sur le bouton Chiffrer/Déchiffrer.\n-Si vous souhaitez la déchiffrer entrez la clé de déchiffrage dans le champ Clé et cliquez ensuite sur Chiffrer/Déchiffrer.\n\nNote :\n-Les fichiers de sorties (image (dé)chiffrée et clé) sont trouvable au même endroit que le programme.")

def browse() : #fonction selection image a chiffrer
    file = filedialog.askopenfilename(initialdir = "/",title = "Choisi une image",filetypes = (("Image","*.jpg"),("Image","*.png"),("Image","*.jpeg"))) #ouvre fenetre pour selec img
    if file == "" :
        path.configure(text = "...") #modif affichage
    else :
        path.configure(text = file) #affiche chemin sur dans interface
    
def crypt() : #fonction chiffrer
    if path.cget("text") == "..." : #verif si img selectionné
        messagebox.showerror("Erreur", "Aucune image selectionée.\nVeuillez réessayer.")
    else :
        i = Image.open(path.cget("text"))
        print(path.cget("text"))
        #fonction chiffrement ici
        
        largeur, hauteur = i.size
        print (largeur,hauteur)
        x=0
        y=0
        liste=[]
        somme=0
        VALprofondeur=len(i.getpixel((0,0)))    #on affecte le nbr de valeurs que possèdent un pixel de l'image à VALprofondeur (si elle possède 3 valeurs RGB, 4 valeurs TRGB etc...)
        for a in range(0,VALprofondeur):        #étape (A)
             temp=[]                            #On crée autant de listes que le pixel a de valeurs. On les stocke dans une autre liste.
             liste.append(temp)
        for y in range(hauteur):
             for x in range(largeur):               #on crée une double boucle pour parcourir pixel par pixel, toute l'image.
                  profondeur = i.getpixel((x,y))    #on stocke les valeurs du pixel à la position (x,y) (donc en fonction des boucles) dans la variable profondeur.
                  liste2=()                 #on initialise un tuple qui se réinitialisera lors de l'exécution des boucles. (tuple = une liste MAIS ne peut pas etre modifiée et a des () )
                  for idc in range(0,VALprofondeur):    #la boucle s'éxécute le nombre de fois que le pixel a de valeurs. (par exemple : 3 fois pour une image en profondeur de couleur 24)
                       hasd = (randint(0,255)-profondeur[idc])  #on crée une valeur aléatoire entre 0 et 255 (minimum et maximum de la valeur de couleur d'une image)
                       somme=somme+hasd                         #et on y retire la valeur du pixel de la valeur rouge, vert, bleu etc en fonction de son nombre de valeurs.
                                                                #(pour que la somme de ces valeurs ne soit pas supérieure à 255)
                       liste[idc].append(hasd)                  #on ajoute ces valeurs aléatoires dans une liste contenant le nombre de listes créées lors de l'étape(A)                                          
                       liste2=liste2+(profondeur[idc]+liste[idc][len(liste[idc])-1],)
                  i.putpixel((x,y),liste2)
                  
        fin=path.cget("text")[-1]
        form=""                         
        k=-1
        print(path.cget("text"))
        while(fin!="."):
            form=fin.upper() + form
            k=k-1
            fin=path.cget("text")[k]    
        nomfichier=""
        while(fin!="/"):
            nomfichier=fin + nomfichier
            k=k-1
            fin=path.cget("text")[k]       
        liste.append(str(bin(abs(somme))))
        print(str(bin(abs(somme))))
        form="png"
        nomfichier=os.path.join(path.cget("text")[0:k],"crypt_"+nomfichier+form.lower())
        print(nomfichier)
       
    
        with ouvrir("donnees", 'ab') as fichier:
            mon_pickler = pickle.Pickler(fichier) #on enregistre les valeurs de la liste dans un fichier de données qui sera utilisé pour le déchiffrement.
            mon_pickler.dump(liste)
      
        i.save(nomfichier,"PNG")
        txtinput.configure(state = "normal")
        txtinput.insert(END, str(bin(abs(somme))))
        txtinput.configure(state = "disabled")
        messagebox.showinfo("Succès !", "Le chiffrement s'est déroulé avec succès !\nVeuillez retrouver les images (dé)chiffrés dans le dossier du programme.")

def uncrypt() : #fonction déchiffrer
    if path.cget("text") == "..." : #verif si img selectionné
        messagebox.showerror("Erreur", "Aucune image selectionée.\nVeuillez réessayer.")
    else :
        i = Image.open(path.cget("text"))
        if str(key.get()) == "" : #si aucune clé est entrée
            messagebox.showerror("Erreur", "Aucune clé n'a été entrée.\nVeuillez réessayer.")
        else :
            #fonction déchiffrement ici
            cryptage_recupere = []

            with ouvrir('donnees', 'rb') as fichier:
                 mon_depickler = pickle.Unpickler(fichier)                  
                 while(True):
                      try:
                           cryptage_recupere.append(mon_depickler.load())   
                      except EOFError:
                           break
            oh=len(cryptage_recupere)
            fin=path.cget("text")[-1]
            form=""
            k=-1
            print(path.cget("text"))
            while(fin!="."):
                form=fin.upper() + form
                k=k-1
                fin=path.cget("text")[k]
            nomfichier=""
            while(fin!="/"):
                nomfichier=fin + nomfichier
                k=k-1
                fin=path.cget("text")[k]
            nomfichier2=nomfichier[5:len(nomfichier)]+str(key.get())
            check=False
            enreg=0
            for j in range(0,len(cryptage_recupere)):

                if (key.get() != cryptage_recupere[j][len(cryptage_recupere[j])-1]):  
                    
                    continue
                else:
                    enreg=j
                    check=True 
                    break
            if (not check) :
                messagebox.showerror("Erreur", "Une mauvaise clé a été entrée. Veuillez réessayer.")
                return

            listedecryptage=cryptage_recupere[enreg]


            largeur, hauteur = i.size
            VALprofondeur=len(i.getpixel((0,0)))
            x=0
            y=0
            u=0
            for y in range(hauteur):
                 for x in range(largeur):
                      profondeur = i.getpixel((x,y))
                      liste3=()
                      for puts in range(0,VALprofondeur):                               #processus inverse de lors du cryptage
                           liste3=liste3+(profondeur[puts]-listedecryptage[puts][u],)
                      i.putpixel((x,y),liste3)
                      u=u+1
              
          
            form="png"    
            nomfichier=os.path.join(path.cget("text")[0:k],"decrypt_"+nomfichier+form.lower())
            print(nomfichier)
##            if(form=="JPG"):
##                form="JPEG"
            i.save(nomfichier,"PNG") 
            messagebox.showinfo("Succès !", "Le déchiffrement s'est déroulé avec succès !\nVeuillez retrouver les images (dé)chiffrés dans le dossier du programme.")
            path.configure(text = "...")

def error() : #message d'erreur si aucune selection
    messagebox.showerror("Erreur", "Aucune méthode selectionée.\nVeuillez réessayer.")
        
def sel() : #active champ texte uniquement déchiffrer
    if str(var.get()) == "1" : 
        btncrypt.configure(command = crypt)
        mode = "chiffrer"
        txtinput.configure(state = "disabled")
    if str(var.get()) == "2" : 
        btncrypt.configure(command = uncrypt)
        mode = "déchiffrer"
        txtinput.configure(state = "normal") 
    #selection = "\n\nVous avez choisi de " + mode + "."
    #choix.configure(text = selection)

#interface
file = ""
Label(window, text = "Ce programme est capable de (dé)chiffrer une image en changeant la couleur de chaque pixels de l'image.").grid(row = 0)
casePath = Label(window, text = "")
casePath.grid(row = 3)
Label(casePath, text = "\nVeuillez choisir une image :").grid()
path = Label(casePath, text = "...")
path.grid(row = 1)
btnpath = Button(window, text = "Parcourir...", command = browse)
btnpath.grid(row = 5)
choix = Label(window, text = "\n\nChiffrer ou déchiffrer ?")
choix.grid(row = 7)
caseRadio = Label(window, text = "")
caseRadio.grid(row = 8)
var = IntVar()
Radiobutton(caseRadio, text = "Chiffrer", variable = var, value = 1, command = sel).grid(column = 0, row = 0)
Radiobutton(caseRadio, text = "Déchiffrer", variable = var, value = 2, command = sel).grid(column = 0, row = 1)
caseKey = Label(window, text = "")
caseKey.grid(row = 9)
Label(caseKey, text = "Clé : ").grid(column = 0, row = 0)
key = StringVar()
txtinput = Entry(caseKey, textvariable = key, state = "disabled")
txtinput.grid(column = 1, row = 0)
btncrypt = Button(window, text = "Chiffrer/Déchiffrer", command = error)
btncrypt.grid(row = 11)
Label(window).grid(row = 10) #espaces pour arranger
##T = Text(window, height=2, width=30)
##T.grid(row=12)

Label(window).grid(row = 12)
Label(window).grid(row = 13)
Label(window).grid(row = 14)
Label(window).grid(row = 16)
caseAbout = Label(window)
caseAbout.grid(row = 15)
Button(caseAbout, text = "À propos", width = 7, command = about).grid(column = 0, row = 0)
Label(caseAbout).grid(column = 1, row = 0)
Button(caseAbout, text = "Aide ?", width = 7, command = help).grid(column = 2, row = 0)


ttk.Progressbar(window, orient = "horizontal",length = screenw/2).grid(row = 17) #barre de progression servant uniquement a centre les widgets car on utilise grid

window.mainloop()








