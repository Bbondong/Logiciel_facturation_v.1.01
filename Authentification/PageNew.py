from tkinter import *
from customtkinter import * 
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from src.factur import  generer_double_facture, enregistrer_afficher_et_supprimer_facture
from database import get_connection
from src.SidebarMenu import SidebarMenu
from datetime import datetime
import random
import string
from tkinter.ttk import Treeview
                

articles_tableaux = []
quantites = []
prixs = []
reduction =""
class PageNew(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
    def update_matricule(self):
            utilisateur = self.controller.utilisateur_connecte
            self.controller.protocol("WM_DELETE_WINDOW", lambda: None)
            Nom_Agent = utilisateur[3]
            Matric = utilisateur[1]
            if utilisateur:
                
                conn = get_connection()
                cursor = conn.cursor()
             # Creation u conteneur initial
                Conteneur_init = Frame(self, background="white", width="1200", height="740")
                Conteneur_init.pack()

                # Sidebar menu
                sidebar = SidebarMenu(self, self.controller, utilisateur, Nom_Agent)
                sidebar.place(x=0, y=0)
                
                
                # Information clint
                def information_clint(*args):
                    # information client
                    nom_client = nom.get()
                    num_client = num.get()
                    Adresse_client = Adresse.get()
                    
                    # Tableau 
                    
    
                
                def Nom_articl():
                    return combo.get()

                def ajouter_article():
                    article = Nom_articl()
                    qte = var_qte.get()
                    prix = entry_prix.get()
                    nom_client = nom.get()
                    num_client = num.get()
                    Adresse_client = Adresse.get()
                    nom_client = nom_client.strip()
                    Adresse_client = Adresse_client.strip()
                    
                    
                    variable = {
                        'Identite du client': nom_client,
                        'Numero du client': num_client,
                        'Adresse du client': Adresse_client
                    }
                    
                    # Détecter les champs vides
                    champs_vides = [Nom for Nom, val in variable.items() if not val]
                    
                    if champs_vides:
                        messagebox.showerror(
                            'Erreur de saisie',
                            f"Erreur : les champs suivants sont vides :\n- " + "\n- ".join(champs_vides)
                        )
                    else:
                        variables = {"article": article, "quantite de l'article": qte, 'prix': prix}
                        if any(not v for v in variables.values()):
                            for noms, val in variables.items():
                                if not val:
                                    messagebox.showerror('Erreur de saisie', f'Erreur : les champs suivantes sont vides :{noms}')
                        else:
                            champs = [
                                nom,
                                num,
                                Adresse,
                                devise
                            ]
                            for champ in champs:
                                champ.configure(state="disabled")

                            # # Stocker les données
                            articles_tableaux.append(article)
                            quantites.append(qte)
                            prixs.append(prix)

                            #  Réinitialiser les champs
                            var_qtes.set("")
                            var_prix.set("")
                    
                var_qtes = StringVar()
                var_prix = StringVar()
                
                
                    
                nom_clint = StringVar()
                nom_clint.trace_add("write", information_clint)
                
                
                num_clint = StringVar()
                num_clint.trace_add("write", information_clint)
                
                Adresse_clint = StringVar()
                Adresse_clint .trace_add("write", information_clint)
                
                # FOnction imprim
                
                # Cod
               
                def generer_code_facture_unique(cursor, length=5):
                    caracteres = string.ascii_uppercase + string.digits

                    while True:
                        conn = get_connection()
                        cursor = conn.cursor()
                        code = ''.join(random.choices(caracteres, k=length))
                        cursor.execute("SELECT COUNT(*) FROM Client WHERE id_client = ?", (code,))
                        if cursor.fetchone()[0] == 0:
                            return code

                                                # Rduciton
                def afficher_verification_articles():
                    original_prixs = prixs.copy()
                    reduction = "Non"

                    # Fenêtre
                    fenetre = CTkToplevel()
                    fenetre.title("Vérification des Articles")
                    fenetre.geometry("600x400")

                    # Tableau
                    tree = Treeview(fenetre, columns=("Article", "Quantité", "Prix"), show="headings", height=8)
                    tree.heading("Article", text="Article")
                    tree.heading("Quantité", text="Quantité")
                    tree.heading("Prix", text="Prix")

                    # Entrées modifiables (une par prix)
                    prix_entries = []

                    for i in range(len(articles_tableaux)):
                        tree.insert("", "end", values=(articles_tableaux[i], quantites[i], prixs[i]))

                    tree.pack(pady=10)

                    # Section modification
                    frame_inputs = CTkFrame(fenetre)
                    frame_inputs.pack(pady=10)

                    for i in range(len(articles_tableaux)):
                        lbl = CTkLabel(frame_inputs, text=f"Prix modifié pour {articles_tableaux[i]}:")
                        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")

                        entry = CTkEntry(frame_inputs)
                        entry.insert(0, str(prixs[i]))
                        entry.grid(row=i, column=1, padx=10, pady=5)
                        prix_entries.append(entry)

                    # Résultat affichage
                    label_reduction = CTkLabel(fenetre, text="Réduction : Non")
                    label_reduction.pack(pady=10)

                    # Boutons
                    def confirmer():
                        global reduction
                        nouvelle_liste_prix = []
                        for i, entry in enumerate(prix_entries):
                            try:
                                nouveau_prix = float(entry.get())
                                if nouveau_prix < float(original_prixs[i]):
                                    reduction = "Oui"
                                nouvelle_liste_prix.append(nouveau_prix)
                                prixs.append(nouveau_prix)
                            except ValueError:
                                nouvelle_liste_prix.append(float(original_prixs[i]))  # Valeur par défaut si erreur

                        label_reduction.configure(text=f"Réduction : {reduction}")
                        # Mise à jour des prix
                        prixs[:] = nouvelle_liste_prix
                        fenetre.destroy()

                    def fermer():
                        fenetre.destroy()

                    bouton_confirmer = CTkButton(fenetre, text="Confirmer", command=confirmer)
                    bouton_confirmer.pack(side="left", padx=20, pady=10)

                    bouton_fermer = CTkButton(fenetre, text="Fermer", command=fermer)
                    bouton_fermer.pack(side="right", padx=20, pady=10)
                       
                def imprim():
                    global articles_tableaux, quantites, prixs
                    
                    nom_client = nom.get()
                    num_client = num.get()
                    Adresse_client = Adresse.get()
                    
                    # rqt pour recupere le info
                    cursor.execute("SELECT Nom_entreprise, Adresse_entreprise, Num_entreprise FROM entreprise WHERE id_entreprise = 1")
                    resultat = cursor.fetchone()

                    nom_entreprise = resultat[0]
                    adresse_entreprise = resultat[1]
                    num_entreprise = resultat[2]
                    
                    entreprise_info = {
                        "nom": nom_entreprise,
                        "adresse":adresse_entreprise,
                        "siren": num_entreprise,
                    }
                    entreprise_info_str = (
                        f"{entreprise_info['nom']}\n"
                        f"{entreprise_info['adresse']}\n"
                        f"numero : {entreprise_info['siren']}\n"
                    )
                    client_info = f"Nom : {nom_client}\nTéléphone : {num_client}\nAdresse : {Adresse_client}"
                    
                    if not articles_tableaux and not quantites and not prixs:
                        messagebox.showerror("Erreur", "Veuillez cliquer sur Ajoute un article et Recomencer !")
                    else: 
                        # Recupere 2 premier valeur du nom de client 
                        code_Factur = generer_code_facture_unique(cursor)
                        cursor.execute("INSERT INTO Client (id_client, identite_client, Numero_client, Adresse_client, matricul) VALUES (?, ?, ?, ?, ?)", (code_Factur, nom_client, num_client, Adresse_client, Matric))
                        conn.commit()
                        # Facture
                        separateur = "*"
                        # Encodage : liste -> chaîne
                        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        articles_str = separateur.join(articles_tableaux)
                        quantites_str = separateur.join(str(q) for q in quantites)
                        prixs_str = separateur.join(str(p) for p in prixs)
                        devise = TAUX()
                        print(reduction)
                        cursor.execute("INSERT INTO Facture (Nom_article, Quantite_article, Prix_init, date_facture, id_client, devise, reduction) VALUES (?, ?, ?, ?, ?,?,?)", (articles_str, quantites_str, prixs_str, date_heure, code_Factur, devise, reduction))
                        conn.commit()
                        # Reconvertir en listes
                        # Tu décompresses directement à partir des chaînes déjà en mémoire
                        articles_tableaux = articles_str.split(separateur)
                        quantites = [int(q) for q in quantites_str.split(separateur)]
                        prixs = [float(p) for p in prixs_str.split(separateur)]
                        print(prixs)
                        pdf_buffer = generer_double_facture(entreprise_info_str, client_info, articles_tableaux, quantites, prixs, code_Factur, devise, reduction)
                        # Exemple : écrire temporairement pour test (à supprimer plus tard)
                        enregistrer_afficher_et_supprimer_facture("facture.pdf", pdf_buffer)
                        articles_tableaux.clear()
                        quantites.clear()
                        prixs.clear()
                     

                # Factur
                Conteneur_facture = CTkFrame(sidebar, width=753 , height=530,  bg_color="white", fg_color="#FFFFFF")
                Conteneur_facture.place(x=320,y=200)
                
                # Factur cod
                def get_next_facture_id():
                    cursor.execute("SELECT TOP 1 id_facture FROM Facture ORDER BY id_facture DESC")
                    result = cursor.fetchone()  # fetchone() suffit ici
                
                    if result:
                        dernier_id = result[0]
                    else:
                        dernier_id = 0
                
                    next_id = dernier_id + 1
                    return str(next_id).zfill(3)
                
                # Après chaque insertion dans la table Facture :
                Factur = get_next_facture_id()

                
                Txt_Factu =Label(Conteneur_facture, text=f"Facture N° : {Factur}",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 21))
                Txt_Factu.place(x=20, y=0)
                
                Txt_identite =Label(Conteneur_facture, text="Identite du client :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_identite.place(x=20, y=41)
                
                
                # Champs :
                
                nom = CTkEntry(Conteneur_facture, font=("Microsoft YaHei UI Light", 17), width=290, height=50,  border_color="black", fg_color="white", textvariable=nom_clint)
                nom.place(x=20,y=75)
                
                # Num
                
                def valider_chiffres(proposition):
                    return proposition.isdigit() or proposition == ""
                
                vcmd = self.register(valider_chiffres)
                
                Txt_num =Label(Conteneur_facture, text="Numero du client    :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_num.place(x=20, y=180)
                
                # Champs :
                
                num = CTkEntry(Conteneur_facture, font=("Microsoft YaHei UI Light", 15), width=130, height=45,  border_color="black", fg_color="white" ,  validate="key", validatecommand=(vcmd, "%P"),  textvariable=num_clint)
                num.place(x=185,y=140)
                
                # Adresse
                
                Txt_adr =Label(Conteneur_facture, text="Adresse du client   :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_adr.place(x=20, y=250)
                
                  # Champs :
                
                Adresse = CTkEntry(Conteneur_facture, font=("Microsoft YaHei UI Light", 15), width=290, height=45,  border_color="black", fg_color="white",  textvariable=Adresse_clint)
                Adresse.place(x=20,y=250)
                
                
                # Information sur la commande :
                
                Txt_identite_com =Label(Conteneur_facture, text="Information sur la commande :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 20))
                Txt_identite_com.place(x=390, y=39)
                
                # Nom articl
                
                Txt_nom_articl =Label(Conteneur_facture, text="Nom de l'article            :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_nom_articl.place(x=410, y=75)
                
                def afficher_prix(event=None):
                    nom_article = combo.get()
                    prix = articles_prix.get(nom_article, "")
                    
                cursor.execute("SELECT Nom_article, Prix_article FROM Article")
                articles = cursor.fetchall()
                
                articles_prix = {nom: prix for nom, prix in articles}

                # Liste des noms pour la Combobox
                noms_articles = list(articles_prix.keys())
                
                combo = CTkComboBox(Conteneur_facture, values=noms_articles, state="readonly", command=afficher_prix)
                combo.place(x=600, y=65)
                

                # Quantit
                
                Txt_Qt_articl =Label(Conteneur_facture, text="Quantite de l'article      :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_Qt_articl.place(x=410, y=140)
                
                
                
                var_qte= CTkEntry(Conteneur_facture, font=("Microsoft YaHei UI Light", 15), width=130 ,height=30,  border_color="black", fg_color="white",  validate="key", validatecommand=(vcmd, "%P"), textvariable=var_qtes)
                var_qte.place(x=600, y=109)
                
                # Prix articl
                
                Txt_nom =Label(Conteneur_facture, text="Prix de l'article a l'unit  :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_nom.place(x=410, y=180)
                
                # Prix articl
                

                entry_prix = CTkEntry(Conteneur_facture,  font=("Microsoft YaHei UI Light", 15), width=130 ,height=30,  border_color="black", fg_color="white", textvariable=var_prix)
                entry_prix.place(x=600, y=144)
                
                if noms_articles:
                    combo.set(noms_articles[0])
                    afficher_prix()
                
                # Prix total articl
                
                Txt_nom =Label(Conteneur_facture, text="Prix Total de l'article    :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_nom.place(x=410, y=225)
                
                # Champ total
                def TAUX():
                    return devise.get()
                    
                
                def calcul_total(*args):
                    Taux_jour = TAUX()
                    if Taux_jour == "Dollars":
                        try:
                            qte = int(var_qte.get())
                            prix = float(entry_prix.get())
                            total = qte * prix
                            var_total.set(f"{total:.2f}")
                        except ValueError:
                            var_total.set("")
                    else:
                        cursor.execute("SELECT Taux_jour FROM Taux where id_taux = 1")
                        Resultat = cursor.fetchall()
                        Taux = Resultat[0][0]
                        try:
                            qte = int(var_qte.get())
                            prix = float(entry_prix.get())
                            prix =  Taux * prix
                            total = qte * prix
                            var_total.set(f"{total:.2f}")
                        except ValueError:
                            var_total.set("")   
            
                var_total = StringVar()
                
                entry_total = CTkEntry(Conteneur_facture, textvariable=var_total, state="readonly")
                entry_total.place(x=600, y=179)
                
                var_qte.bind("<KeyRelease>", calcul_total)
                entry_prix.bind("<KeyRelease>", calcul_total)
                # Devise
                
                Txt_nom =Label(Conteneur_facture, text="Devise de l'article        :",fg="black", background="#FFFFFF" ,font=("Bahnschrift", 18))
                Txt_nom.place(x=410, y=265)
                
                Taux = ['Dollars', 'Franc_Congolais']
                
                devise = CTkComboBox(Conteneur_facture, values=Taux, state="readonly")
                devise.place(x=600,y=214)
                devise.set(Taux[0]) 
                # Creation de bouton
                
                CTkButton(Conteneur_facture, text="Ajoute un article" , corner_radius=10, fg_color="#0F64C5", bg_color="white", text_color="black", hover_color="#0F64C5", command=ajouter_article).place(x=250, y=350)
                
                CTkButton(Conteneur_facture, text="Reduction" , corner_radius=10, fg_color="#C20A0A", bg_color="white", text_color="black", hover_color="#C20A0A", command=afficher_verification_articles).place(x=430, y=350)
                
                CTkButton(Conteneur_facture, text="Imprime la facture" , corner_radius=10, fg_color="#0F9E05", bg_color="white", text_color="black", hover_color="#0F9E05", command=imprim).place(x=600, y=350)
                footer_text = "Version 1.1 - Développé par Ben tech / Beny Badibanga, dev full stack"
                footer = Label(Conteneur_facture, text=footer_text, font=("Arial", 10), fg="gray")
                footer.place(x=50, y=580)     
            else:
                print("Error Pas d'Agent")

      