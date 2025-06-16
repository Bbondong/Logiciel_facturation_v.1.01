from tkinter import *
from customtkinter import * 
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from src.SidebarMenu import SidebarMenu
from database import get_connection
from src.factur import generer_double_facture, enregistrer_afficher_et_supprimer_facture
from datetime import datetime
from calendar import monthrange

class PageList(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def update_matricule(self):
        self.controller.protocol("WM_DELETE_WINDOW", lambda: None)
        utilisateur = self.controller.utilisateur_connecte
        Nom_Agent = utilisateur[3] if utilisateur else None
        if utilisateur:
            # Création du conteneur principal
            Conteneur_init = Frame(self, background="white", width=1200, height=740)
            Conteneur_init.pack()

            sidebar = SidebarMenu(self, self.controller, utilisateur, Nom_Agent)
            sidebar.place(x=0, y=0)

            Conteneur_Valeur = CTkFrame(sidebar, width=853, height=530, bg_color="white", fg_color='white')
            Conteneur_Valeur.place(x=320, y=220)

            # Titre "Liste de facture"
            List = CTkLabel(Conteneur_Valeur, text="Liste de facture", text_color="#000000", bg_color="white", font=("Bahnschrift", 19))
            List.place(x=10, y=10)

            # Titre "Rechercher"
            List = CTkLabel(Conteneur_Valeur, text="Rechercher", text_color="#000000", bg_color="white", font=("Bahnschrift", 19))
            List.place(x=400, y=10)

            # Fonction de validation
            def valider_recherche():
                code = Code_Facture.get().strip()
                if not code:
                    messagebox.showwarning("Attention", "Veuillez entrer un code de facture.")
                    return
                try:
                    conn = get_connection()
                    cursor = conn.cursor()

                    # Recherche sécurisée avec paramètre (évite injection)
                    cursor.execute("SELECT id_client FROM Client WHERE id_client = ?", (code,))
                    result = cursor.fetchone()

                    if result:
                        id_client_trouve = result[0]
                        imprimer_facture(id_client_trouve)
                    else:
                        messagebox.showinfo("Information", f"Aucune facture trouvée pour le code : {code}")

                except Exception as e:
                    print(e)
                    messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

            # Champ Code Facture
            Code_Facture = CTkEntry(Conteneur_Valeur, font=("Microsoft YaHei UI Light", 15), width=140, height=30, border_color="black", fg_color="white")
            Code_Facture.place(x=510, y=10)

            CTkButton(Conteneur_Valeur, text="Valider", corner_radius=2, fg_color="#3ADB16", bg_color="white", text_color="black", hover_color="#00E331", command=valider_recherche).place(x=660, y=10)

            # Connexion à la base
            conn = get_connection()
            cursor = conn.cursor()

            # Date actuelle
            now = datetime.now()

            # Premier jour du mois actif
            date_debut = now.replace(day=1).strftime("%Y-%m-%d")

            # Dernier jour du mois actif (calculé dynamiquement)
            dernier_jour = monthrange(now.year, now.month)[1]
            date_fin = now.replace(day=dernier_jour).strftime("%Y-%m-%d")

            cursor.execute("""
                SELECT f.id_client, c.identite_client, f.[Nom_article], f.[Quantite_article], f.[Prix_init]
                FROM Client AS c, Facture AS f
                WHERE f.id_client = c.id_client
                AND f.date_facture BETWEEN ? AND ?
            """, (date_debut, date_fin))

            factures = cursor.fetchall()

            # Zone avec scroll
            zone_scroll = CTkFrame(Conteneur_Valeur, width=900, height=530, fg_color="white")
            zone_scroll.place(x=0, y=50)

            canvas = Canvas(zone_scroll, bg="white", width=1000, height=530, highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = Scrollbar(zone_scroll, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)

            conteneur_factures = Frame(canvas, bg="white")
            window_id = canvas.create_window((0, 0), window=conteneur_factures, anchor="nw")

            def update_scroll(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(window_id, width=canvas.winfo_width())
            conteneur_factures.bind("<Configure>", update_scroll)

            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

            # Affichage factures (affiche seulement nombre d'articles)
            for code, nom_client, articles_str, quantites_str, prixs_str in factures:
                separateur = "*"
                articles_tableaux = str(articles_str).split(separateur)
                nombre_articles = len(articles_tableaux)

                ligne = Frame(conteneur_factures, bg="white", width=830)
                ligne.pack(pady=10, padx=10, anchor="w")

                facture_frame = CTkFrame(
                    ligne,
                    fg_color="#297CBF",
                    corner_radius=10,
                    width=597,
                    height=100
                )
                facture_frame.pack(side="left")

                Label(facture_frame, text=f"Facture : {code}", bg="#297CBF", fg="white", font=("Arial", 12, "bold")).place(x=20, y=10)
                Label(facture_frame, text=f"Client : {nom_client}", bg="#297CBF", fg="white", font=("Arial", 11)).place(x=20, y=35)
                Label(facture_frame, text=f"Nombre d'articles : {nombre_articles}", bg="#297CBF", fg="white", font=("Arial", 11)).place(x=20, y=60)

                btn = CTkButton(ligne, text="Imprimer", width=150, height=40, fg_color="#24B916",
                                command=lambda c=code: imprimer_facture(c))
                btn.pack(side="left", padx=(20, 0))

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

            def imprimer_facture(code_facture):
                conn = get_connection()
                cursor = conn.cursor()

                # Récupération des infos entreprise
                cursor.execute("SELECT Nom_entreprise, Adresse_entreprise, Num_entreprise FROM entreprise WHERE id_entreprise = 1")
                resultat = cursor.fetchone()
                entreprise_info = {
                    "nom": resultat[0],
                    "adresse": resultat[1],
                    "siren": resultat[2],
                }
                entreprise_info_str = (
                    f"{entreprise_info['nom']}\n"
                    f"{entreprise_info['adresse']}\n"
                    f"Numéro : {entreprise_info['siren']}\n"
                )

                # Requête pour récupérer la facture et les infos client associées
                cursor.execute("""
                    SELECT f.id_facture, f.Nom_article, f.Quantite_article, f.Prix_init, f.date_facture, f.devise, f.reduction,
                           c.id_client, c.identite_client, c.Numero_client, c.Adresse_client
                    FROM Facture AS f, Client AS c
                    WHERE f.id_client = c.id_client AND f.id_client = ?
                """, (code_facture,))

                resultat = cursor.fetchone()
                if not resultat:
                    print("Facture non trouvée")
                    return

                (id_facture, articles_str, quantites_str, prixs_str, date_facture, devise, reduction,
                 id_client, identite_client, numero_client, adresse_client) = resultat

                separateur = "*"
                articles_tableaux = str(articles_str).split(separateur)
                quantites = [int(q) for q in str(quantites_str).split(separateur)]
                prixs = [float(p) for p in str(prixs_str).split(separateur)]

                client_info = (
                    f"{identite_client}\n"
                    f"{adresse_client}\n"
                    f"Téléphone : {numero_client}\n"
                    f"Date : {date_facture.strftime('%d/%m/%Y') if hasattr(date_facture, 'strftime') else date_facture}"
                )

                pdf_buffer = generer_double_facture(entreprise_info_str, client_info, articles_tableaux, quantites, prixs, id_client, devise, reduction)

                enregistrer_afficher_et_supprimer_facture("facture.pdf", pdf_buffer)

        else:
            print("Error Pas d'Agent")
