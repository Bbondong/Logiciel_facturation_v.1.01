import io
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime
import webbrowser
from pathlib import Path
import sys

def generer_double_facture(entreprise_info, client_info, articles_tableaux, quantites, prixs, code_factur, devise, reduction):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largeur, hauteur = A4

    symbole = "$" if devise.lower() == "dollars" else "Fc"

    # Résolution du chemin Asset (compatible PyInstaller)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    logo_path = os.path.join(base_path, "Asset", "logo_profil.jpg")

    def dessiner_facture(y_offset):
        # Logo
        try:
            c.drawImage(logo_path, 20 * mm, hauteur - (40 * mm) - y_offset, width=30 * mm, height=30 * mm, mask='auto')
        except Exception as e:
            print(f"Erreur chargement logo : {e}")

        # Code facture (haut droit)
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(195 * mm, hauteur - (20 * mm) - y_offset, f"Facture N° {code_factur}")

        # Infos entreprise
        c.setFont("Helvetica", 10)
        for i, line in enumerate(entreprise_info.split("\n")):
            c.drawString(60 * mm, hauteur - (30 + i * 5) * mm - y_offset, line)

        # Infos client
        c.drawString(60 * mm, hauteur - (50 * mm) - y_offset, "Client :")
        client_info_lines = client_info.split("\n")
        for i, line in enumerate(client_info_lines):
            c.drawString(60 * mm, hauteur - (55 + i * 5) * mm - y_offset, line)

        # Date
        y_fin_client = hauteur - (55 + (len(client_info_lines) * 5)) * mm - y_offset
        y_date = y_fin_client - (5 * mm)
        c.drawString(20 * mm, y_date, f"Date d’émission : {datetime.today().strftime('%d/%m/%Y')}")

        # En-têtes tableau
        y_tableau = y_date - (10 * mm)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(20 * mm, y_tableau, "Désignation")
        c.drawString(90 * mm, y_tableau, "Qté")
        c.drawString(110 * mm, y_tableau, "Prix Unit.")
        c.drawString(140 * mm, y_tableau, "Total")

        # Lignes article
        c.setFont("Helvetica", 9)
        total_ht = 0
        for i, (article, qte, prix) in enumerate(zip(articles_tableaux, quantites, prixs)):
            y = y_tableau - ((5 + i * 7) * mm)
            c.drawString(20 * mm, y, str(article))
            c.drawString(90 * mm, y, str(int(qte)))
            c.drawString(110 * mm, y, f"{float(prix):.2f} {symbole}")
            c.drawString(140 * mm, y, f"{float(prix) * int(qte):.2f} {symbole}")
            total_ht += float(prix) * int(qte)

        # Total HT
        y_total = y_tableau - ((5 + len(articles_tableaux) * 7) * mm) - (10 * mm)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(140 * mm, y_total, f"Total HT : {total_ht:.2f} {symbole}")

        # TVA et message
        c.setFont("Helvetica", 8)
        c.drawString(20 * mm, y_total - (10 * mm), "TVA non applicable")
        c.drawString(20 * mm, y_total - (15 * mm), "Marchandises vendues ni reprises ni échangées.")

        # Réduction
        if reduction.strip().lower() == "oui":
            c.setFont("Helvetica-Bold", 9)
            c.setFillColorRGB(0, 0.5, 0)
            c.drawString(20 * mm, y_total - (25 * mm), "Vous avez eu une réduction.")
            c.setFillColorRGB(0, 0, 0)

    dessiner_facture(0)
    dessiner_facture(148 * mm)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def afficher_facture(pdf_filename):
    pdf_file = Path(__file__).parent / pdf_filename
    pdf_file = pdf_file.resolve()

    if not pdf_file.is_file():
        messagebox.showerror("Erreur", f"Fichier introuvable : {pdf_file}")
        return

    try:
        webbrowser.open(pdf_file.as_uri())
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")

def enregistrer_afficher_et_supprimer_facture(pdf_filename, pdf_buffer):
    pdf_path = Path(__file__).parent / pdf_filename
    with open(pdf_path, "wb") as f:
        f.write(pdf_buffer.read())

    afficher_facture(pdf_filename)

    def supprimer_apres_delai():
        time.sleep(60)  # Délai en secondes
        try:
            if pdf_path.exists():
                pdf_path.unlink()
        except Exception as e:
            print(f"Erreur lors de la suppression automatique : {e}")

    threading.Thread(target=supprimer_apres_delai, daemon=True).start()
