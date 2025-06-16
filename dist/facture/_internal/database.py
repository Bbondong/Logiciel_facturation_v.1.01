import pyodbc
import os
from datetime import datetime
from tkinter import messagebox


def get_connection():
    try:
        # Obtenir le chemin du répertoire où se trouve ce fichier .py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construire le chemin complet vers la base de données
        db_path = os.path.join(base_dir, 'data', 'Data.accdb')
        
        # Créer la chaîne de connexion
        connexion_bd = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={db_path};'
        )
        conn = pyodbc.connect(connexion_bd)
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Erreur de connexion", f"Impossible de se connecter à la base de données.\n\n{e}")
        return None   
        # Connexion à la base
    
def verification_utilisateur(Matricul, Password):
    conn = get_connection()
    cursor = conn.cursor()
    rqt_sql = "SELECT * FROM Agent WHERE Matricul = ? AND Password = ?"
    cursor.execute(rqt_sql, (Matricul, Password))

    user = cursor.fetchone()

    if user:
        conn.close()
        return user
    else:
        messagebox.showerror("Error", "Matricul ou mot de passe incorrect.")


