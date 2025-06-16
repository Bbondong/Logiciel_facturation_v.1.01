import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageTk
import os
import sys

class SidebarMenu(ctk.CTkFrame):
    def __init__(self, parent, controller, utilisateur, Nom_Agent):
        super().__init__(parent, width=10000, height=1240, fg_color="#FFFFFF")
        self.controller = controller
        self.utilisateur = utilisateur
        self.Nom_Agent = Nom_Agent

        # Chemin de base (compatible PyInstaller)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # Conteneur sidebar (canvas)
        conteneur = Canvas(self, width=350, height=1000, highlightthickness=0)
        conteneur.place(x=0, y=0)

        # Image de fond
        bg_path = os.path.join(base_path, "Asset", "Rectangle.png")
        bg_image = Image.open(bg_path).resize((500, 1050))
        bg_photo = ImageTk.PhotoImage(bg_image)
        conteneur.create_image(0, 0, anchor="nw", image=bg_photo)
        conteneur.bg_photo = bg_photo

        # Stocker les images pour éviter le garbage collection
        conteneur.image_store = []

        # Boutons du menu
        self.add_canvas_button(conteneur, os.path.join(base_path, "Asset", "Accueil.png"), "Accueil", 300, self.go_home, image_size=(50, 45), text_color='#FFFFFF')
        self.add_canvas_button(conteneur, os.path.join(base_path, "Asset", "File.png"), "Nouvelle Facture", 400, self.go_facture, image_size=(50, 45), text_color='#FFFFFF')
        self.add_canvas_button(conteneur, os.path.join(base_path, "Asset", "List.png"), "List Facture", 500, self.go_list, image_size=(50, 45), text_color='#FFFFFF')
        self.add_canvas_button(conteneur, os.path.join(base_path, "Asset", "Sortie.png"), "Déconnexion", 850, self.logout, text_color="red", image_size=(80, 45))

        # Section Dashboard (en haut à droite)
        dashboard_canvas = Canvas(self, width=1020, height=400, highlightthickness=0, bg="#FFFFFF")
        dashboard_canvas.place(x=400, y=0)

        header_path = os.path.join(base_path, "Asset", "Groupes.png")
        header_img = Image.open(header_path).resize((970, 200))
        header_tk = ImageTk.PhotoImage(header_img)
        dashboard_canvas.create_image(0, 0, anchor="nw", image=header_tk)
        dashboard_canvas.header = header_tk

        dashboard_canvas.create_text(20, 20, anchor="nw", text="Dashboard", fill="#FFFFFF", font=("Bahnschrift", 20))
        dashboard_canvas.create_text(20, 65, anchor="nw",
            text=f"Bienvenue, {Nom_Agent} ! Nous sommes ravis de vous voir.",
            fill="#FFFFFF", font=("Suwannaphum", 13))
        dashboard_canvas.create_text(20, 90, anchor="nw",
            text="Voici votre tableau de bord personnalisé pour une gestion",
            fill="#FFFFFF", font=("Suwannaphum", 13))
        dashboard_canvas.create_text(20, 115, anchor="nw", text="efficace et rapide.",
            fill="#FFFFFF", font=("Suwannaphum", 13))

    def add_canvas_button(self, canvas, image_path, text, y, command, text_color="black", underline=False, image_size=(30, 30)):
        # Charger l’image
        try:
            icon = Image.open(image_path).resize(image_size)
            icon_tk = ImageTk.PhotoImage(icon)
            canvas.image_store.append(icon_tk)
        except Exception as e:
            print(f"Erreur chargement image {image_path} : {e}")
            return

        image_x = 25
        image_y = y
        canvas.create_image(image_x, image_y, anchor="nw", image=icon_tk)

        text_x = image_x + image_size[0] + 10
        text_y = y + (image_size[1] // 2)

        font_style = ("Arial", 16, "underline") if underline else ("Arial", 16)
        canvas.create_text(text_x, text_y, anchor="w", text=text, font=font_style, fill=text_color)

        # Zone cliquable
        click_area = canvas.create_rectangle(10, y, 300, y + image_size[1], outline="", fill="", tags="btn")
        canvas.tag_bind(click_area, "<Button-1>", lambda event: command())

    def go_home(self):
        self.controller.utilisateur_connecte = self.utilisateur
        self.controller.show_frame("PageAccueil")
        self.controller.frames["PageAccueil"].update_matricule()

    def go_facture(self):
        self.controller.utilisateur_connecte = self.utilisateur
        self.controller.show_frame("PageNew")
        self.controller.frames["PageNew"].update_matricule()

    def go_list(self):
        self.controller.utilisateur_connecte = self.utilisateur
        self.controller.show_frame("PageList")
        self.controller.frames["PageList"].update_matricule()

    def logout(self):
        from tkinter import messagebox
        messagebox.showinfo('Valider', f'À très bientôt !, {self.Nom_Agent}')
        self.controller.quit()
