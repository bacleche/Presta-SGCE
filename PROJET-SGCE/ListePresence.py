import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer

# Fonction de connexion à la base de données
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='SGCE'
        )
        return connection
    except pymysql.MySQLError as e:
        messagebox.showerror("Erreur de connexion", f"Erreur de connexion à la base de données: {e}")
        return None

# Enregistrement de présence
def enregistrer_presence(etudiant_id, classe):
    connection = get_db_connection()
    if connection:
        try:
            today = datetime.now().date()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM presence WHERE etudiant_id = %s AND date = %s", (etudiant_id, today))
                result = cursor.fetchone()
                
                if result:
                    messagebox.showwarning("Présence déjà enregistrée", "L'étudiant est déjà enregistré aujourd'hui.")
                else:
                    heure_arrivee = datetime.now().strftime("%H:%M:%S")
                    statut = "Présent"
                    cursor.execute(
                        "INSERT INTO presence (etudiant_id, date, classe, heure_arrivee, statut) VALUES (%s, %s, %s, %s, %s)",
                        (etudiant_id, today, classe, heure_arrivee, statut)
                    )
                    connection.commit()
                    messagebox.showinfo("Enregistrement réussi", "Présence enregistrée avec succès.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Erreur de requête", f"Erreur lors de l'enregistrement de la présence: {e}")
        finally:
            connection.close()

# Récupération des classes distinctes
def get_classes():
    connection = get_db_connection()
    classes = []
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT classe FROM presence")
                classes = [row[0] for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            messagebox.showerror("Erreur de requête", f"Erreur lors de la récupération des classes: {e}")
        finally:
            connection.close()
    return classes

# Affichage de la présence pour une classe donnée
def show_class_presence(classe):
    for widget in content_frame.winfo_children():
        widget.destroy()

    columns = ("Etudiant ID", "Date", "Heure d'arrivée", "Statut")
    presence_tree = ttk.Treeview(content_frame, columns=columns, show="headings")

    for col in columns:
        presence_tree.heading(col, text=col)
        presence_tree.column(col, width=150)

    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT etudiant_id, date, heure_arrivee, statut FROM presence WHERE classe = %s", (classe,))
                data = cursor.fetchall()
                for item in data:
                    presence_tree.insert("", tk.END, values=item)
        except pymysql.MySQLError as e:
            messagebox.showerror("Erreur de requête", f"Erreur lors de la récupération des données: {e}")
        finally:
            connection.close()

    presence_tree.pack(fill="both", expand=True, padx=20, pady=(20, 5))

    # Bouton pour générer la liste de présence
    generate_button = tk.Button(content_frame,  font="Shrikhand", text="Générer liste de présence", command=lambda: generate_presence_list(classe))
    generate_button.pack(pady=(5, 20))

# Génération du document PDF avec la liste de présence
def generate_presence_list(classe):
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                # Jointure avec la table "etudiants" pour récupérer le nom et le prénom
                cursor.execute("""
                    SELECT p.etudiant_id, e.nom, e.prenom, p.date, p.heure_arrivee, p.statut
                    FROM presence p
                    JOIN etudiant e ON p.etudiant_id = e.id
                    WHERE p.classe = %s AND p.date = CURDATE()
                """, (classe,))

                data = cursor.fetchall()

                # En-tête du tableau, avec les colonnes nom et prénom
                pdf_data = [["Etudiant ID", "Nom", "Prenom", "Date", "Heure d'arrivée", "Statut", "C1", "C2", "C3", "C4"]]
                for row in data:
                    # Ajoutez 4 cases à cocher vides pour chaque occurrence de présence
                    pdf_data.append(list(row) + ["☐", "☐", "☐", "☐"])

                # Demander à l'utilisateur où enregistrer le PDF
                pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                         filetypes=[("PDF files", "*.pdf")],
                                                         title="Enregistrer la liste de présence sous")
                if not pdf_file:  # Si l'utilisateur annule
                    return

                doc = SimpleDocTemplate(pdf_file, pagesize=letter)
                table = Table(pdf_data)
                styles = getSampleStyleSheet()
                title_style = styles['Title']

                title = Paragraph(f"Liste de Présence pour la Classe {classe}", title_style)
                spacer = Spacer(1, 12)  # Espace de 12 points
                
                # Style du tableau
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),  # Augmenter la taille de la police
                ])
                table.setStyle(style)

                # Construire le PDF
                doc.build([title, spacer, table])
                messagebox.showinfo("PDF généré", f"La liste de présence a été générée : {os.path.abspath(pdf_file)}")

        except pymysql.MySQLError as e:
            messagebox.showerror("Erreur de requête", f"Erreur lors de la génération de la liste de présence: {e}")
        finally:
            connection.close()


# Création des boutons dynamiques pour chaque classe
def create_class_buttons():
    classes = get_classes()
    for classe in classes:
        button = tk.Button(button_frame, text=f"Présence {classe}",  font="Shrikhand",command=lambda c=classe: show_class_presence(c))
        button.pack(side=tk.LEFT, padx=5, pady=5)

# Fenêtre principale
root = tk.Tk()
root.title("Gestion des Présences par Classe **Presta**")
root.geometry("800x600")

# Cadre pour les boutons de classe
button_frame = tk.Frame(root, bg="lightgrey")
button_frame.pack(fill="x", padx=20, pady=10)

# Cadre pour le contenu principal
content_frame = tk.Frame(root, bg="white")
content_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Créer dynamiquement les boutons pour chaque classe
create_class_buttons()

# Lancement de l'application Tkinter
root.mainloop()
