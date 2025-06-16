# Importation de la bibliotheque Tkinter et autre bibliotheque
from tkinter import *
from customtkinter import *
from Authentification.PageConnexion import PageConnexion
from Authentification.PageAcceuil import PageAccueil
from Authentification.PageList import PageList
from Authentification.PageNew import PageNew
from src.SidebarMenu import SidebarMenu

import tkinter.font as tkFont
import os
import datetime
import socket
import json
import sys
import shutil
from tkinter import messagebox
import base64
import stat

# Définition du chemin vers la police
police_path = os.path.join("Asset", "Police", "Suwannaphum.ttf")
if not os.path.exists(police_path):
    print("La police spécifiée n'existe pas.")

# === Début de la logique de licence (sécurisée) ===
CONFIG_DIR = os.path.join(os.getenv("APPDATA") or os.getcwd(), ".bentech")  # dossier masqué
CONFIG_PATH = os.path.join(CONFIG_DIR, "syscfg.b64")  # nom obscur
LIMIT_DAYS = 3
MAX_TRIES = 5

def get_machine_id():
    return socket.gethostname()

def save_config(config):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        encoded = base64.b64encode(json.dumps(config).encode("utf-8")).decode("utf-8")
        with open(CONFIG_PATH, "w") as f:
            f.write(encoded)
        try:
            os.chmod(CONFIG_PATH, stat.S_IREAD)
        except:
            pass
    except Exception as e:
        print(f"Erreur sauvegarde : {e}")

def load_config():
    try:
        if not os.path.exists(CONFIG_PATH):
            return None
        with open(CONFIG_PATH, "r") as f:
            encoded = f.read()
        decoded = base64.b64decode(encoded).decode("utf-8")
        return json.loads(decoded)
    except Exception as e:
        print(f"Erreur lecture config : {e}")
        return None

def uninstall():
    try:
        if os.path.exists(CONFIG_DIR):
            shutil.rmtree(CONFIG_DIR)
        shutil.rmtree(os.getcwd())
    except Exception as e:
        print(f"Erreur désinstallation : {e}")

def show_license_window(lancer_app):
    tries = [0]
    fenetre = CTk()
    fenetre.title("Activation")
    fenetre.geometry("400x240")
    fenetre.resizable(False, False)

    label_info = CTkLabel(fenetre, text="Entrez votre code de licence :", font=CTkFont(size=16))
    label_info.pack(pady=10)

    entry_code = CTkEntry(fenetre, font=CTkFont(size=14), justify='center')
    entry_code.pack(pady=5)

    essais_restants = CTkLabel(fenetre, text=f"Essais restants : {MAX_TRIES}", font=CTkFont(size=14))
    essais_restants.pack(pady=5)

    def valider_code():
        code = entry_code.get().strip()
        if code not in ["1234", "Mukulubeny13@"]:
            tries[0] += 1
            restant = MAX_TRIES - tries[0]
            essais_restants.configure(text=f"Essais restants : {restant}")
            if tries[0] >= MAX_TRIES:
                messagebox.showerror("Erreur", "Essais dépassés. Désinstallation.")
                fenetre.destroy()
                uninstall()
                sys.exit()
            else:
                messagebox.showerror("Erreur", f"Code invalide. Il vous reste {restant} essai(s).")
            return
        today = datetime.date.today().isoformat()
        config = {
            "license_key": code,
            "install_date": today,
            "activated": code == "bentech",
            "machine_id": get_machine_id()
        }
        save_config(config)
        fenetre.destroy()
        lancer_app()

    CTkButton(fenetre, text="Valider", command=valider_code).pack(pady=10)
    fenetre.mainloop()

def check_license(lancer_app):
    config = load_config()
    current_machine_id = get_machine_id()
    if not config:
        show_license_window(lancer_app)
        return
    if config.get("machine_id") != current_machine_id:
        messagebox.showerror("Erreur", "Licence invalide sur cette machine.")
        uninstall()
        sys.exit()
    if config["license_key"] == "bentech":
        lancer_app()
    elif config["license_key"] == "1234":
        install_date = datetime.date.fromisoformat(config["install_date"])
        days_passed = (datetime.date.today() - install_date).days
        if days_passed > LIMIT_DAYS:
            show_license_window(lancer_app)
        else:
            lancer_app()
    else:
        messagebox.showerror("Erreur", "Licence corrompue.")
        sys.exit()
# === Fin de la logique de licence ===

# Classe principale
class Main(CTk):
    def __init__(self):
        super().__init__()
        self.title('Facture')
        self.geometry("1200x740")
        self.resizable(False, False)
        container = Frame(self)
        container.pack(fill="both", expand=True)

        self.utilisateur_connecte = None
        self.frames = {}

        for F in (PageConnexion, PageAccueil, PageList, PageNew):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageConnexion")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Point d'entrée principal
def lancer_app():
    app = Main()
    app.mainloop()

if __name__ == "__main__":
    check_license(lancer_app)
