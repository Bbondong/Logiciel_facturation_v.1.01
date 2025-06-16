from tkinter import *
from customtkinter import * 
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from database import get_connection
from src.SidebarMenu import SidebarMenu

class PageAccueil(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def update_matricule(self):
            utilisateur = self.controller.utilisateur_connecte
            self.controller.protocol("WM_DELETE_WINDOW", lambda: None)
            Nom_Agent = utilisateur[3]
            Matric = utilisateur[1]
            if utilisateur:
                
                
             # Creation u conteneur initial
                Conteneur_init = Frame(self, background="white", width="1200", height="740")
                Conteneur_init.pack()
                
                
                 # Sidebar menu
                sidebar = SidebarMenu(self, self.controller, utilisateur, Nom_Agent)
                sidebar.place(x=0, y=0)
                
                
                
                # Conteneur Valeur   
                Conteneur_Valeur= CTkFrame(sidebar,width=800 , height=530,  bg_color="white", fg_color='white')
                Conteneur_Valeur.place(x=320,y=220)
                
                
              
                # Dashoard reste
                
    
                # List Facture crée
                
                rectangle_frame1 = CTkFrame(Conteneur_Valeur, 
                    width=350, 
                    height=139, 
                    corner_radius=13,
                    fg_color="#ffffff",
                    border_width=1.5,
                    border_color='black'
                )
                rectangle_frame1.place(x=38, y=25) 
                
                # Txt 
                
                Txt_list = Label(rectangle_frame1, text="Liste de facture créer", background='white',fg="black" ,font=("Atomic Age", 15))
                Txt_list.place(x=65, y=20)
                
                # boucle pour affiche Nbr client
                Txt_list = Label(rectangle_frame1, text="0", background='white', fg="black", font=("Atomic Age", 25))
                Txt_list.place(x=160, y=60)
                
                def update_count():
                    conn = get_connection()
                    cursor = conn.cursor()
                    requete = "SELECT COUNT(*) FROM Client WHERE matricul = ?;"
                    cursor.execute(requete, (Matric,))
                    resultat = cursor.fetchone()[0]
                    cursor.close()
                    conn.close()
                
                    Txt_list.config(text=f"{resultat}")
                    rectangle_frame1.after(1000, update_count)  # relance la fonction toutes les 1 seconde
                
                update_count()
                form1 = CTkFrame(rectangle_frame1, width=30, height=30, fg_color="#2FC20E", bg_color="#ffffff", corner_radius=50)
                form1.place(x=20, y=65)
                
                
                # List CLient enregistre
                
                rectangle_frame2 = CTkFrame(Conteneur_Valeur, 
                    width=350, 
                    height=139, 
                    corner_radius=13,
                    fg_color="#ffffff",
                    border_width=1.5,
                    border_color='black'
                )
                rectangle_frame2.place(x=420, y=25) 
                
                # Txt 
                
                Txt_client = Label(rectangle_frame2, text="Liste des client enregistrer", background='white',fg="black" ,font=("Atomic Age", 15))
                Txt_client.place(x=65, y=20)
                
                conn = get_connection()
                cursor = conn.cursor()
                requete2 = "SELECT COUNT(*) FROM Client WHERE matricul = ?;"
                cursor.execute(requete2, (Matric,))
                resultat = cursor.fetchone()[0]
             
                
                Txt_list = Label(rectangle_frame2, text=f"{resultat}", background='white',fg="black" ,font=("Atomic Age", 25))
                Txt_list.place(x=160, y=60)
                
                form2 = CTkFrame(rectangle_frame2, width=30, height=30, fg_color="red", bg_color="#ffffff", corner_radius=50)
                form2.place(x=20, y=65)
                       
            else:
                print("Error Pas d'Agent")

      