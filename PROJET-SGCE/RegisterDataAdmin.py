import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import pymysql
from pymysql import Error
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from tkinter import filedialog , messagebox
from datetime import datetime
import pandas as pd

# Connexion à la base de données MySQL avec pymysql
def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            database='SGCE',
            user='root',  # Remplace 'root' par ton nom d'utilisateur MySQL
            password=''  # Remplace 'password' par ton mot de passe MySQL
        )
        if connection.open:
            print("Connexion à MySQL réussie")
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None




# Fonction pour convertir la date au format MySQL (YYYY-MM-DD)
def convert_date_to_mysql_format(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        print(f"Erreur de conversion de la date: {date_str}")
        return None

# # Fonction pour ajouter un étudiant à la base de données et au Treeview
# def add_student():
#     connection = connect_to_db()
#     if connection is None:
#         return

#     try:
#         cursor = connection.cursor()

#         nom_value = entry_nom.get()
#         prenom_value = entry_prenom.get()
#         date_frequentation_value = entry_date_frequentation.get()
#         email = entry_email.get()
#         adresse = entry_adresse.get()
#         telephone_value = entry_telephone.get()
#         classe_value = combobox_classe.get()
#         filiere_value = combobox_filiere.get()
#         niveau_value = combobox_niveau.get()
#         option_value = combobox_option.get()

#         date_frequentation_value_mysql = convert_date_to_mysql_format(date_frequentation_value)
#         if date_frequentation_value_mysql is None:
#             print("Format de date invalide")
#             return

#         # Vérifiez la classe et récupérez son ID
#         cursor.execute("SELECT classe_id FROM Classe WHERE libelle = %s", (classe_value,))
#         classe_id_row = cursor.fetchone()
#         if classe_id_row:
#             classe_id = classe_id_row[0]
#         else:
#             print("Classe sélectionnée invalide")
#             return
        
#         cursor.execute("SELECT niveau_id FROM Niveau WHERE libelle = %s", (niveau_value,))
#         niveau_id_row = cursor.fetchone()
#         if niveau_id_row:
#             niveau_id = niveau_id_row[0]
#         else:
#             print("Niveau sélectionnée invalide")
#             return
        
#         cursor.execute("SELECT options_id FROM Options WHERE libelle = %s", (option_value,))
#         option_id_row = cursor.fetchone()
#         if option_id_row:
#             option_id = option_id_row[0]
#         else:
#             print("Options sélectionnée invalide")
#             return
        
#         cursor.execute("SELECT filiere_id FROM Filiere WHERE libelle = %s", (filiere_value,))
#         filiere_id_row = cursor.fetchone()
#         if filiere_id_row:
#             filiere_id = filiere_id_row[0]
#         else:
#             print("Filière sélectionnée invalide")
#             return

#         # Générer le code QR
        

#         # Récupérer l'année actuelle
#         current_year = datetime.now().year

#         # Compter le nombre d'étudiants déjà enregistrés pour générer un ID unique
#         cursor.execute("SELECT MAX(CAST(SUBSTRING(id, 8, 2) AS UNSIGNED)) FROM etudiant WHERE id LIKE %s", (f'ET{current_year}&%',))
#         max_position_number = cursor.fetchone()[0] or 0  # S'il n'y a pas d'étudiants, commencez à 0
#         position_number = max_position_number + 1  # Incrémenter le max trouvé

#         # Générer l'ID
#         student_id = f"ET{current_year}&{str(position_number).zfill(2)}"  # Zfill pour avoir deux chiffres
        
        
#         qr_img = generate_qr_code(student_id + ' '+ nom_value + ' ' + prenom_value+ ' ' +niveau_value+ ' ' +filiere_value+ ' ' +classe_value+ ' ' +option_value)
#         qr_img_bytes = qr_img_to_base64(qr_img)
#         # Insérer les données dans la table étudiant
#         insert_query = """
#         INSERT INTO etudiant (id, nom, prenom, email, telephone, adresse, date_frequentation, classe, filiere, niveau, options, qr_code, admin_id)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
#         """
#         cursor.execute(insert_query, (student_id, nom_value, prenom_value, email, telephone_value, adresse, date_frequentation_value_mysql, classe_id, filiere_id, niveau_id, option_id, qr_img_bytes))
#         connection.commit()

#         # Ajouter les valeurs au Treeview
#         tree.insert("", tk.END, values=(student_id, nom_value, prenom_value, email, adresse, classe_value, filiere_value, niveau_value))

#         # Afficher le code QR en temps réel sur le canvas
#         display_qr_code(qr_img_bytes)

#     except Error as e:
#         print(f"Erreur lors de l'insertion de l'étudiant: {e}")
#         connection.rollback()
#     finally:
#         if connection.open:
#             cursor.close()
#             connection.close()

#     # Effacer les champs d'entrée après l'enregistrement
#     entry_nom.delete(0, tk.END)
#     entry_prenom.delete(0, tk.END)
#     entry_date_frequentation.delete(0, tk.END)
#     entry_email.delete(0, tk.END)
#     entry_adresse.delete(0, tk.END)
#     entry_telephone.delete(0, tk.END)
#     combobox_classe.set('')
#     combobox_filiere.set('')
#     combobox_niveau.set('')
#     combobox_option.set('')



# Fonction pour ajouter un étudiant à la base de données et au Treeview
# def add_student():
#     connection = connect_to_db()
#     if connection is None:
#         return

#     try:
#         cursor = connection.cursor()

#         nom_value = entry_nom.get()
#         prenom_value = entry_prenom.get()
#         date_frequentation_value = entry_date_frequentation.get()
#         email = entry_email.get()
#         adresse = entry_adresse.get()
#         telephone_value = entry_telephone.get()
#         classe_value = combobox_classe.get()
#         filiere_value = combobox_filiere.get()
#         niveau_value = combobox_niveau.get()
#         option_value = combobox_option.get()
#         image_path = entry_image_path.get()  # Récupérer le chemin de l'image

#         # Convertir la date pour MySQL
#         date_frequentation_value_mysql = convert_date_to_mysql_format(date_frequentation_value)
#         if date_frequentation_value_mysql is None:
#             print("Format de date invalide")
#             return

#         # Vérifiez et récupérez les IDs des autres tables
#         cursor.execute("SELECT classe_id FROM Classe WHERE libelle = %s", (classe_value,))
#         classe_id = cursor.fetchone()
#         if not classe_id:
#             print("Classe invalide")
#             return
#         classe_id = classe_id[0]

#         cursor.execute("SELECT niveau_id FROM Niveau WHERE libelle = %s", (niveau_value,))
#         niveau_id = cursor.fetchone()
#         if not niveau_id:
#             print("Niveau invalide")
#             return
#         niveau_id = niveau_id[0]

#         cursor.execute("SELECT options_id FROM Options WHERE libelle = %s", (option_value,))
#         option_id = cursor.fetchone()
#         if not option_id:
#             print("Option invalide")
#             return
#         option_id = option_id[0]

#         cursor.execute("SELECT filiere_id FROM Filiere WHERE libelle = %s", (filiere_value,))
#         filiere_id = cursor.fetchone()
#         if not filiere_id:
#             print("Filière invalide")
#             return
#         filiere_id = filiere_id[0]

#         # Générer l'ID de l'étudiant
#         current_year = datetime.now().year
#         cursor.execute("SELECT MAX(CAST(SUBSTRING(id, 8, 2) AS UNSIGNED)) FROM etudiant WHERE id LIKE %s", (f'ET{current_year}&%',))
#         max_position_number = cursor.fetchone()[0] or 0
#         position_number = max_position_number + 1
#         student_id = f"ET{current_year}&{str(position_number).zfill(2)}"

#         # Générer le QR code
#         qr_img = generate_qr_code(student_id + ' ' + nom_value + ' ' + prenom_value+ ' ' +niveau_value+ ' ' +filiere_value+ ' ' +classe_value+ ' ' +option_value)
#         qr_img_bytes = qr_img_to_base64(qr_img)

#         # Convertir l'image en binaire
#         if image_path:
#             with open(image_path, 'rb') as file:
#                 image_data = file.read()
#         else:
#             image_data = None

#         # Insérer les données dans la base
#         insert_query = """
#         INSERT INTO etudiant (id, nom, prenom, email, telephone, adresse, date_frequentation, classe, filiere, niveau, options, images, qr_code, admin_id)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
#         """
#         cursor.execute(insert_query, (student_id, nom_value, prenom_value, email, telephone_value, adresse, date_frequentation_value_mysql, classe_id, filiere_id, niveau_id, option_id, qr_img_bytes, image_data))
#         connection.commit()

#         # Ajouter l'étudiant au Treeview
#         tree.insert("", tk.END, values=(student_id, nom_value, prenom_value, email, adresse, classe_value, filiere_value, niveau_value))

#         # Afficher le QR code en temps réel sur le canvas
#         display_qr_code(qr_img_bytes)

#     except Error as e:
#         print(f"Erreur lors de l'insertion de l'étudiant: {e}")
#         connection.rollback()
#     finally:
#         if connection.open:
#             cursor.close()
#             connection.close()

#     # Effacer les champs d'entrée après l'enregistrement
#     entry_nom.delete(0, tk.END)
#     entry_prenom.delete(0, tk.END)
#     entry_date_frequentation.delete(0, tk.END)
#     entry_email.delete(0, tk.END)
#     entry_adresse.delete(0, tk.END)
#     entry_telephone.delete(0, tk.END)
#     entry_image_path.delete(0, tk.END)  # Effacer le champ image
#     combobox_classe.set('')
#     combobox_filiere.set('')
#     combobox_niveau.set('')
#     combobox_option.set('')




def add_student():
    connection = connect_to_db()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        nom_value = entry_nom.get()
        prenom_value = entry_prenom.get()
        date_frequentation_value = entry_date_frequentation.get()
        email = entry_email.get()
        adresse = entry_adresse.get()
        telephone_value = entry_telephone.get()
        classe_value = combobox_classe.get()
        filiere_value = combobox_filiere.get()
        niveau_value = combobox_niveau.get()
        option_value = combobox_option.get()
        image_path = entry_image_path.get()  # Récupérer le chemin de l'image

        date_frequentation_value_mysql = convert_date_to_mysql_format(date_frequentation_value)
        if date_frequentation_value_mysql is None:
            print("Format de date invalide")
            return

        # Vérification des IDs dans la base de données
        cursor.execute("SELECT classe_id FROM Classe WHERE libelle = %s", (classe_value,))
        classe_id_row = cursor.fetchone()
        if classe_id_row:
            classe_id = classe_id_row[0]
        else:
            print("Classe sélectionnée invalide")
            return

        cursor.execute("SELECT niveau_id FROM Niveau WHERE libelle = %s", (niveau_value,))
        niveau_id_row = cursor.fetchone()
        if niveau_id_row:
            niveau_id = niveau_id_row[0]
        else:
            print("Niveau sélectionné invalide")
            return

        cursor.execute("SELECT options_id FROM Options WHERE libelle = %s", (option_value,))
        option_id_row = cursor.fetchone()
        if option_id_row:
            option_id = option_id_row[0]
        else:
            print("Option sélectionnée invalide")
            return

        cursor.execute("SELECT filiere_id FROM Filiere WHERE libelle = %s", (filiere_value,))
        filiere_id_row = cursor.fetchone()
        if filiere_id_row:
            filiere_id = filiere_id_row[0]
        else:
            print("Filière sélectionnée invalide")
            return

        # Récupérer l'année actuelle
        current_year = datetime.now().year

        # Générer un ID étudiant unique
        cursor.execute("SELECT MAX(CAST(SUBSTRING(id, 8, 2) AS UNSIGNED)) FROM etudiant WHERE id LIKE %s", (f'ET{current_year}&%',))
        max_position_number = cursor.fetchone()[0] or 0
        position_number = max_position_number + 1
        student_id = f"ET{current_year}&{str(position_number).zfill(2)}"

        # Générer le QR Code
        qr_img = generate_qr_code(student_id + ' ' + nom_value + ' ' + prenom_value + ' ' + niveau_value + ' ' + filiere_value + ' ' + classe_value + ' ' + option_value)
        qr_img_bytes = qr_img_to_base64(qr_img)
        
        # Insérer l'étudiant avec le chemin de l'image
        insert_query = """
        INSERT INTO etudiant (id, nom, prenom, email, telephone, adresse, date_frequentation, classe, filiere, niveau, options, images,  qr_code, admin_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  NULL)
        """
        cursor.execute(insert_query, (student_id, nom_value, prenom_value, email, telephone_value, adresse, date_frequentation_value_mysql, classe_id, filiere_id, niveau_id, option_id,image_path, qr_img_bytes))
        connection.commit()

        # Ajouter l'étudiant au Treeview
        tree.insert("", tk.END, values=(student_id, nom_value, prenom_value, email, adresse, classe_value, filiere_value, niveau_value))

        # Afficher le code QR en temps réel
        display_qr_code(qr_img_bytes)

    except Error as e:
        print(f"Erreur lors de l'insertion de l'étudiant: {e}")
        connection.rollback()
    finally:
        if connection.open:
            cursor.close()
            connection.close()

    # Effacer les champs après l'ajout
    entry_nom.delete(0, tk.END)
    entry_prenom.delete(0, tk.END)
    entry_date_frequentation.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_adresse.delete(0, tk.END)
    entry_telephone.delete(0, tk.END)
    combobox_classe.set('')
    combobox_filiere.set('')
    combobox_niveau.set('')
    combobox_option.set('')
    entry_image_path.delete(0, tk.END)  # Réinitialiser le champ image




# Fonction pour générer et retourner l'image du code QR
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# Convertir l'image QR en Base64
def qr_img_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Convertir une image Base64 en image PIL
def base64_to_image(base64_str):
    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data))
    return image

# Afficher l'image QR sur le Canvas
def display_qr_code(qr_code_base64):
    qr_img = base64_to_image(qr_code_base64)
    qr_img = qr_img.resize((300, 250))
    qr_img_tk = ImageTk.PhotoImage(qr_img)
    qr_canvas.create_image(0, 0, anchor=tk.NW, image=qr_img_tk)
    qr_canvas.image = qr_img_tk


def afficher_image(img_path):
    if os.path.exists(img_path):  
        img = Image.open(img_path)
        print(f"Image chargée : {img.size}, mode {img.mode}")  # Vérifier la taille et le mode
        img = img.resize((300, 250))  

        img_tk = ImageTk.PhotoImage(img)
        img_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)  
        img_canvas.image = img_tk  # Prévenir le garbage collector
        
    else:
        print("Image introuvable")

# # Charger le code QR de l'étudiant sélectionné
# def on_tree_select(event):
#     selected_item = tree.selection()
#     if not selected_item:
#         return
    
#     item = selected_item[0]
#     student_id = tree.item(item, 'values')[0]

#     connection = connect_to_db()
#     if connection is None:
#         return

#     try:
#         cursor = connection.cursor()
#         select_query = "SELECT qr_code FROM etudiant WHERE id = %s"
#         cursor.execute(select_query, (student_id,))
#         result = cursor.fetchone()
        
#         cursor = connection.cursor()
#         select_query = "SELECT images FROM etudiant WHERE id = %s"
#         cursor.execute(select_query, (student_id,))
#         img = cursor.fetchone()

#         if result:
#             qr_code_base64 = result[0]
#             img=img[0]
#             display_qr_code(qr_code_base64)
#             afficher_image(img)
            
#         else:
#             qr_canvas.delete("all")
#     except Error as e:
#         print(f"Erreur lors de la récupération du code QR: {e}")
#     finally:
#         if connection.open:
#             cursor.close()
#             connection.close()


def on_tree_select(event):
    selected_item = tree.selection()
    if not selected_item:
        return
    
    item = selected_item[0]
    student_id = tree.item(item, 'values')[0]

    connection = connect_to_db()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        
        # Sélectionner à la fois le QR code et l'image dans une seule requête
        select_query = "SELECT qr_code, images FROM etudiant WHERE id = %s"
        cursor.execute(select_query, (student_id,))
        result = cursor.fetchone()

        if result:
            qr_code_base64, img_path = result

            # Afficher le QR Code
            if qr_code_base64:
                display_qr_code(qr_code_base64)
            
            # Afficher l'image si elle existe
            if img_path:
                if os.path.exists(img_path):  # Vérifie si le fichier existe
                    print(f"Chemin de l'image récupéré : {img_path}")

                    afficher_image(img_path)
                else:
                    print(f"Image introuvable : {img_path}")
            else:
                print("Aucune image enregistrée pour cet étudiant.")

        else:
            qr_canvas.delete("all")
            img_canvas.delete("all")
            print("Étudiant non trouvé dans la base.")
            
    except Error as e:
        print(f"Erreur lors de la récupération des données: {e}")
    finally:
        if connection.open:
            cursor.close()
            connection.close()


# Fonction principale pour afficher QR Code et image


# Fonction pour charger les étudiants depuis la base de données et les afficher dans le Treeview
def load_students():
    connection = connect_to_db()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        select_query = "SELECT id, nom, prenom, email, adresse, classe, filiere, niveau FROM etudiant"
        cursor.execute(select_query)
        results = cursor.fetchall()

        # Effacer le Treeview avant de charger les nouvelles données
        tree.delete(*tree.get_children())

        for row in results:
            tree.insert("", tk.END, values=row)

    except Error as e:
        print(f"Erreur lors du chargement des étudiants: {e}")
    finally:
        if connection.open:
            cursor.close()
            connection.close()

def get_qr_image_from_canvas():
    qr_canvas.update()
    canvas_image = qr_canvas.postscript(colormode='color')
    return canvas_image



# Récupérer les données des classes, filières et niveaux
def get_classes():
    connection = connect_to_db()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT libelle FROM Classe")  # Ajustez cela en fonction de votre table
        return [row[0] for row in cursor.fetchall()]  # Renvoie une liste des noms de classe
    except Error as e:
        print(f"Erreur lors de la récupération des classes: {e}")
        return []
    finally:
        if connection.open:
            cursor.close()
            connection.close()

def get_filieres():
    connection = connect_to_db()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT libelle FROM Filiere")  # Remplace 'nom' par le champ approprié de votre table
        return [row[0] for row in cursor.fetchall()]
    except Error as e:
        print(f"Erreur lors de la récupération des filières: {e}")
        return []
    finally:
        if connection.open:
            cursor.close()
            connection.close()

def get_niveaux():
    connection = connect_to_db()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT libelle FROM Niveau")  # Remplace 'nom' par le champ approprié de votre table
        return [row[0] for row in cursor.fetchall()]
    except Error as e:
        print(f"Erreur lors de la récupération des niveaux: {e}")
        return []
    finally:
        if connection.open:
            cursor.close()
            connection.close()
            
            
def get_Options():
    connection = connect_to_db()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT libelle FROM Options")  # Remplace 'nom' par le champ approprié de votre table
        return [row[0] for row in cursor.fetchall()]
    except Error as e:
        print(f"Erreur lors de la récupération des niveaux: {e}")
        return []
    finally:
        if connection.open:
            cursor.close()
            connection.close()


# def print_qr_code():
#     temp_eps_path = "temp_qr_code.eps"
#     qr_canvas.postscript(file=temp_eps_path, colormode='color')
#     qr_img_pil = Image.open(temp_eps_path)
#     temp_png_path = "temp_qr_code.png"
#     qr_img_pil.save(temp_png_path)

#     file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
#     if not file_path:
#         return

#     c = canvas.Canvas(file_path, pagesize=letter)
#     width, height = letter
#     c.drawImage(temp_png_path, 50, height - 300, width=300, height=250)
#     c.save()

#     os.remove(temp_eps_path)
#     os.remove(temp_png_path)

#     print(f"PDF enregistré sous {file_path}")




# def print_qr_code():
#     selected_item = tree.selection()  # Récupérer l'élément sélectionné dans le TreeView
#     if not selected_item:
#         messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant dans la liste.")
#         return

#     student_id = tree.item(selected_item[0], 'values')[0]  # Récupérer l'ID de l'étudiant sélectionné

#     connection = pymysql.connect(host='localhost', user='root', password='', database='SGCE')
#     cursor = connection.cursor()

#     # Récupérer les informations de l'étudiant depuis la base de données
#     cursor.execute("SELECT nom, prenom, email, images, qr_code FROM etudiant WHERE id = %s", (student_id,))
#     student = cursor.fetchone()

#     if not student:
#         messagebox.showerror("Erreur", "Aucun étudiant trouvé avec cet ID.")
#         return

#     nom, prenom, email, img_path, qr_data = student

#     # Vérifier que le fichier image existe
#     if not os.path.exists(img_path):
#         messagebox.showerror("Erreur", f"L'image de l'étudiant est introuvable : {img_path}")
#         return

#     # Demander où enregistrer le fichier PDF
#     file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
#     if not file_path:
#         return

#     c = canvas.Canvas(file_path, pagesize=letter)
#     width, height = letter

#     # Ajouter les informations de l'étudiant
#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(50, height - 100, f"Nom : {nom}")
#     c.drawString(50, height - 120, f"Prénom : {prenom}")
#     c.drawString(50, height - 140, f"Email : {email}")

#     # Ajouter l'image de l'étudiant (utilisation directe du chemin)
#     c.drawImage(img_path, 50, height - 250, width=150, height=150)

#     # Convertir et afficher le QR Code
#     if qr_data:
#         qr_bytes = base64.b64decode(qr_data)
#         qr_img = Image.open(io.BytesIO(qr_bytes))
#         qr_path = "temp_qr_code.jpg"
#         qr_img.save(qr_path, "JPEG")
#         c.drawImage(qr_path, 220, height - 250, width=50, height=50)

#     # Sauvegarder le PDF
#     c.save()

#     # Nettoyage du fichier temporaire QR Code
#     if os.path.exists(qr_path):
#         os.remove(qr_path)

#     cursor.close()
#     connection.close()

#     messagebox.showinfo("Succès", f"Carte d'identité de {prenom} {nom} enregistrée sous {file_path}")

def export_to_excel():
    connection = connect_to_db()
    if not connection:
        messagebox.showerror("Erreur", "Impossible de se connecter à la base de données.")
        return
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nom, prenom, email, adresse, telephone, date_frequentation , classe , filiere , niveau , options FROM etudiant")
            data = cursor.fetchall()
    except pymysql.MySQLError as e:
        messagebox.showerror("Erreur de requête", f"Erreur lors de la récupération des données: {e}")
        return
    finally:
        connection.close()
    
    if not data:
        messagebox.showwarning("Avertissement", "Aucune donnée trouvée dans la base.")
        return

    # Convertir les données en DataFrame Pandas
    df = pd.DataFrame(data, columns=["ID", "Nom", "Prénom", "Email", "Adresse", "Téléphone", "Date de Naissance" , "Classe", "Filière", "Niveau" , "Option"])

    # Demander où sauvegarder le fichier
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    
    if not file_path:
        return

    # Sauvegarde dans un fichier Excel
    try:
        df.to_excel(file_path, index=False, engine="openpyxl")
        messagebox.showinfo("Succès", f"Fichier Excel enregistré avec succès sous {file_path}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la sauvegarde : {e}")


# def print_qr_code():
#     selected_item = tree.selection()
#     if not selected_item:
#         messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant dans la liste.")
#         return

#     student_id = tree.item(selected_item[0], 'values')[0]
    
#     connection = pymysql.connect(host='localhost', user='root', password='', database='SGCE')
#     cursor = connection.cursor()
    
#     cursor.execute("SELECT nom, prenom, email,adresse , telephone , date_frequentation, images, qr_code FROM etudiant WHERE id = %s", (student_id,))
#     student = cursor.fetchone()
    
#     if not student:
#         messagebox.showerror("Erreur", "Aucun étudiant trouvé avec cet ID.")
#         return
    
#     nom, prenom, email,adresse , telephone, date_frequentation, img_path, qr_data = student
    
#     if not os.path.exists(img_path):
#         messagebox.showerror("Erreur", f"L'image de l'étudiant est introuvable : {img_path}")
#         return
    
#     file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
#     if not file_path:
#         return
    
#     c = canvas.Canvas(file_path, pagesize=letter)
#     width, height = letter

#     # Première page (Informations + image)
#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(180, height - 90, f"INSTITUT *THE NAME*")
    
#     c.drawString(220, height - 150, f"Nom : {nom}")
#     c.drawString(220, height - 170, f"Prénom : {prenom}")
#     c.drawString(220, height - 190, f"Email : {email}")
#     c.drawString(220, height - 210, f"Adresse : {adresse}")
#     c.drawString(220, height - 230, f"Telephone : {telephone}")
#     c.drawString(220, height - 250, f"Date de Naissance : {date_frequentation}")
    
#     c.drawImage(img_path,90, height - 230, width=90, height=90)
    
#     c.showPage()  # Ajouter une nouvelle page

#     # Deuxième page (QR Code en grand)
#     if qr_data:
#         qr_bytes = base64.b64decode(qr_data)
#         qr_img = Image.open(io.BytesIO(qr_bytes))
#         qr_path = "temp_qr_code.jpg"
#         qr_img.save(qr_path, "JPEG")
        
#         qr_size = 200
#         qr_x = (width - qr_size) / 2
#         qr_y = (height - qr_size) / 2
#         c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
#         c.drawString(250, height - 500, f"contact@institut.com")
        
#         os.remove(qr_path)
    
#     c.save()
#     cursor.close()
#     connection.close()

#     messagebox.showinfo("Succès", f"Carte d'identité de {prenom} {nom} enregistrée sous {file_path}")

def print_qr_code():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant dans la liste.")
        return

    student_id = tree.item(selected_item[0], 'values')[0]
    
    connection = pymysql.connect(host='localhost', user='root', password='', database='SGCE')
    cursor = connection.cursor()

    # Récupérer les informations de l'étudiant
    cursor.execute("SELECT nom, prenom, email, adresse, telephone, date_frequentation, images, qr_code FROM etudiant WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    
    if not student:
        messagebox.showerror("Erreur", "Aucun étudiant trouvé avec cet ID.")
        return
    
    nom, prenom, email, adresse, telephone, date_frequentation, img_path, qr_data = student

    # Récupérer les informations de l'école
    cursor.execute("SELECT libelle, email, logo FROM ecole LIMIT 1")
    school = cursor.fetchone()
    
    if not school:
        messagebox.showerror("Erreur", "Aucune information d'école trouvée.")
        return

    school_name, school_email , school_logo = school

    if not os.path.exists(img_path):
        messagebox.showerror("Erreur", f"L'image de l'étudiant est introuvable : {img_path}")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Première page (Informations + image)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, height - 90, f"{school_name}")  # Remplace *THE NAME* par le libellé de l'école
    c.drawImage(school_logo, 400, height - 110, width=40, height=40)
    
    
    c.drawString(220, height - 150, f"Nom : {nom}")
    c.drawString(220, height - 170, f"Prénom : {prenom}")
    c.drawString(220, height - 190, f"Email : {email}")
    c.drawString(220, height - 210, f"Adresse : {adresse}")
    c.drawString(220, height - 230, f"Téléphone : {telephone}")
    c.drawString(220, height - 250, f"Date de Naissance : {date_frequentation}")
    
    c.drawImage(img_path, 90, height - 230, width=90, height=90)
    
    c.showPage()  # Ajouter une nouvelle page

    # Deuxième page (QR Code en grand)
    if qr_data:
        qr_bytes = base64.b64decode(qr_data)
        qr_img = Image.open(io.BytesIO(qr_bytes))
        qr_path = "temp_qr_code.jpg"
        qr_img.save(qr_path, "JPEG")
        
        qr_size = 200
        qr_x = (width - qr_size) / 2
        qr_y = (height - qr_size) / 2
        c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
        c.drawString(250, height - 500, school_email)  # Remplace l'email par celui de l'école
        
        os.remove(qr_path)
    
    c.save()
    cursor.close()
    connection.close()

    messagebox.showinfo("Succès", f"Carte d'identité de {prenom} {nom} enregistrée sous {file_path}")



# def choisir_image():
#     chemin = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif")])
#     if chemin:
#         image = Image.open(chemin)
#         image = image.resize((120, 120))  # Redimensionner pour l'affichage
#         photo = ImageTk.PhotoImage(image)
#         label_image.config(image=photo)
#         label_image.image = photo
#         entry_image_path.delete(0, tk.END)
#         entry_image_path.insert(0, chemin)
        
        
        
from tkinter import filedialog
import os

def choisir_image():
    image_path = filedialog.askopenfilename(
        title="Choisir une image", 
        filetypes=[("Tous les fichiers", "*.*")]
    )
    
    if image_path:  # Vérifie si l'image est sélectionnée
        entry_image_path.delete(0, tk.END)
        entry_image_path.insert(0, image_path)  # Afficher le chemin de l'image
        afficher_image(image_path)  # Afficher l'image sélectionnée


# Création de la fenêtre principale
root = tk.Tk()
root.title("Enregistrement des Étudiants **Presta**")
root.geometry("1000x600")

# Cadre pour le formulaire d'enregistrement
form_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
form_frame.pack(padx=10, pady=10, fill="both", expand=True, side="left")

# Labels et champs d'entrée pour les informations des
# Labels et champs d'entrée pour les informations des étudiants
label_nom = tk.Label(form_frame, text="Nom:" , font="Shrikhand")
label_nom.grid(row=0, column=0, sticky=tk.W)
entry_nom = tk.Entry(form_frame)
entry_nom.grid(row=0, column=1, padx=5, pady=5)

label_prenom = tk.Label(form_frame, text="Prénom:",  font="Shrikhand")
label_prenom.grid(row=1, column=0, sticky=tk.W)
entry_prenom = tk.Entry(form_frame)
entry_prenom.grid(row=1, column=1, padx=5, pady=5)

label_date_frequentation = tk.Label(form_frame, font="Shrikhand", text="Date de Naissance (JJ/MM/AAAA):")
label_date_frequentation.grid(row=2, column=0, sticky=tk.W)
entry_date_frequentation = tk.Entry(form_frame)
entry_date_frequentation.grid(row=2, column=1, padx=5, pady=5)

label_email = tk.Label(form_frame, text="Email:", font="Shrikhand")
label_email.grid(row=3, column=0, sticky=tk.W)
entry_email = tk.Entry(form_frame)
entry_email.grid(row=3, column=1, padx=5, pady=5)

label_adresse = tk.Label(form_frame, text="Adresse:",font="Shrikhand")
label_adresse.grid(row=4, column=0, sticky=tk.W)
entry_adresse = tk.Entry(form_frame)
entry_adresse.grid(row=4, column=1, padx=5, pady=5)

label_telephone = tk.Label(form_frame, text="Téléphone:", font="Shrikhand")
label_telephone.grid(row=5, column=0, sticky=tk.W)
entry_telephone = tk.Entry(form_frame)
entry_telephone.grid(row=5, column=1, padx=5, pady=5)

# Ajoutez des combobox pour les classes, filières et niveaux
label_classe = tk.Label(form_frame, text="Classe:", font="Shrikhand")
label_classe.grid(row=6, column=0, sticky=tk.W)
combobox_classe = ttk.Combobox(form_frame, values=get_classes())  # Créez la Combobox ici
combobox_classe.grid(row=6, column=1, padx=5, pady=5)

label_filiere = tk.Label(form_frame, text="Filière:", font="Shrikhand")
label_filiere.grid(row=7, column=0, sticky=tk.W)
combobox_filiere = ttk.Combobox(form_frame, values=get_filieres())  # Créez la Combobox ici
combobox_filiere.grid(row=7, column=1, padx=5, pady=5)

label_niveau = tk.Label(form_frame, text="Niveau:", font="Shrikhand")
label_niveau.grid(row=8, column=0, sticky=tk.W)
combobox_niveau = ttk.Combobox(form_frame, values=get_niveaux())  # Créez la Combobox ici
combobox_niveau.grid(row=8, column=1, padx=5, pady=5)


label_option = tk.Label(form_frame, text="Option:", font="Shrikhand")
label_option.grid(row=9, column=0, sticky=tk.W)
combobox_option = ttk.Combobox(form_frame, values=get_Options())  # Créez la Combobox ici
combobox_option.grid(row=9, column=1, padx=5, pady=5)

label_image_text = tk.Label(form_frame, text="Image de l'étudiant:", font="Shrikhand")
label_image_text.grid(row=10, column=0, sticky=tk.W)

entry_image_path = tk.Entry(form_frame, width=20)
entry_image_path.grid(row=10, column=1, columnspan=2, padx=5, pady=5)  # Étendu sur 2 colonnes pour un meilleur alignement

# Bouton en dessous du champ d'entrée
button_image = tk.Button(form_frame,font="Shrikhand", text="Choisir une image", command=choisir_image)
button_image.grid(row=11, column=1, columnspan=2, pady=5)  # Placé sous le champ

# Zone pour afficher l'image
label_image = tk.Label(form_frame)
label_image.grid(row=12, column=0, columnspan=3, pady=10)  # Placé en dessous avec de l'espace

# Boutons pour ajouter un étudiant et imprimer le QR code
button_add = tk.Button(form_frame, font="Shrikhand", text="Ajouter Étudiant", command=add_student)
button_add.grid(row=13, columnspan=2, pady=10)

button_print = tk.Button(form_frame, font="Shrikhand", text="Genere une carte", command=print_qr_code)
button_print.grid(row=14, columnspan=2, pady=10)

button_print = tk.Button(form_frame, font="Shrikhand", text="Generer en fichier excel", command=export_to_excel)
button_print.grid(row=15, columnspan=2, pady=10)


# Cadre pour afficher le QR code
qr_frame = tk.Frame(root, bg="white", padx=10, pady=10)
qr_frame.pack(padx=15, pady=10, fill="both", expand=True, side="right")

qr_canvas = tk.Canvas(qr_frame, width=300, height=250, bg="white")
qr_canvas.pack()


img_frame = tk.Frame(root, bg="white", padx=10, pady=10)
img_frame.pack(padx=15, pady=17, fill="both", expand=True, side="right")

img_canvas = tk.Canvas(qr_frame, width=300, height=250, bg="white")
img_canvas.pack()

# Cadre pour le Treeview des étudiants
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

# Colonnes du Treeview
columns = ("ID", "Nom", "Prénom", "Email", "Adresse", "Classe", "Filière", "Niveau")
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Définir les en-têtes
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)  # Ajuster la largeur pour un meilleur affichage

# Barre de défilement verticale
scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar_y.set)

# Barre de défilement horizontale
scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
scrollbar_x.pack(fill=tk.X)
tree.configure(xscrollcommand=scrollbar_x.set)
# Lier la sélection d'élément dans le Treeview à la fonction on_tree_select
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Charger les étudiants au démarrage
load_students()

# Démarrer la boucle principale
root.mainloop()
