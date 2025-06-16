from tkinter import *
from customtkinter import * 
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from database import verification_utilisateur
import sys
import os

# Détermination du chemin de base pour les fichiers (images, etc.)
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# Classe Connexion
class PageConnexion(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Fonction de connexion
        def connexion():
            Matricul = user.get().strip()
            Password = Psword.get().strip()
            if Matricul == '' and Password == '':
                messagebox.showerror("Error", "Veuillez remplir les champs vides !") 
            elif Matricul == '':
                messagebox.showerror("Error", "Veuillez remplir le champ Matricul !") 
            elif Password == '':
                messagebox.showerror("Error", "Veuillez remplir le champ Password !") 
            else:
                utilisateur = verification_utilisateur(Matricul, Password)
                if utilisateur:
                    messagebox.showinfo('Valider', f"Bienvenue {utilisateur[3]}")  
                    self.controller.utilisateur_connecte = utilisateur
                    self.controller.show_frame("PageAccueil")
                    self.controller.frames["PageAccueil"].update_matricule()  
                else:
                    messagebox.showerror("Error", "Identifiant incorrect !")              

        # Conteneur principal
        Conteneur_init = Frame(self, background="white", width="10000", height="740")
        Conteneur_init.pack(fill="both", expand=True)

        # Conteneur des champs
        Conteneur_champs = Frame(Conteneur_init, background="white", width="10000", height="1240")
        Conteneur_champs.pack(fill="both", expand=True)

        # Chargement du logo
        logo_path = os.path.join(base_path, "Asset", "logo_profil.jpg")
        image = Image.open(logo_path)
        image = image.resize((150, 150))
        image_tk = ImageTk.PhotoImage(image)
        label = Label(Conteneur_champs, image=image_tk, borderwidth=0, highlightthickness=0)
        label.place(x=50,y=40)
        label.image = image_tk

        # Textes
        Label(Conteneur_champs, text="Get started", fg="#000000", bg="white", font=("Bahnschrift", 15)).place(x=50, y=200)
        Label(Conteneur_champs, text="Welcome to QuickFacture", fg="#000000", bg="white", font=("Bahnschrift", 15)).place(x=50, y=290)
        Frame(Conteneur_champs, width=400, height=2, bg="black").place(x=50, y=240)

        # Champ Matricul
        Label(Conteneur_champs, text="Matricul :", fg="#000000", bg="white", font=("Bahnschrift", 15)).place(x=50, y=370)
        user = CTkEntry(Conteneur_champs, font=("Bahnschrift", 15), width=300, height=45, border_color="black", fg_color="white")
        user.place(x=50, y=330)

        # Champ Password
        Label(Conteneur_champs, text="Password :", fg="#000000", bg="white", font=("Bahnschrift", 15)).place(x=50, y=500)
        Psword = CTkEntry(Conteneur_champs, font=("Bahnschrift", 15), width=300, height=45, border_color="black", fg_color="white")
        Psword.place(x=50, y=440)

        # Bouton de connexion
        CTkButton(
            Conteneur_champs, width=300, text="Sign up", font=('Atomic Age', 25),
            bg_color="white", corner_radius=10, fg_color="#155DE2", height=40,
            command=connexion, text_color="black"
        ).place(x=50, y=570)

        # Chargement de l'image décorative
        cov_path = os.path.join(base_path, "Asset", "cov_png.png")
        img = Image.open(cov_path).resize((800, 800))
        imag_tk = ImageTk.PhotoImage(img)
        Label(Conteneur_init, image=imag_tk, bg="white").place(x=600, y=60)
        # Référence pour éviter le garbage collection
        self.image_ref = imag_tk
        
        footer_text = "Version 1.1 - Développé par Ben tech / Beny Badibanga, dev full stack"
        footer = Label(Conteneur_init, text=footer_text, font=("Arial", 10), fg="gray")
        footer.place(x=50, y=900)

