import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

# Variable globale pour stocker les informations de l'utilisateur connecté
user_info = {}

# Fonction pour se connecter à la base de données
def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',  # Remplace par ton nom d'utilisateur MySQL
            password='',  # Remplace par ton mot de passe MySQL
            database='SGCE'
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

# Fonction pour vérifier si la licence est valide
def is_licence_valid():
    connection = connect_to_db()
    if connection is None:
        messagebox.showinfo("Connexion à la base de données", "L'application n'est pas connectée à la base de données.")
        return False

    try:
        with connection.cursor() as cursor:
            query = "SELECT est_valide FROM Licence LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            return result and result[0] == 1  # Vérifie si est_valide est TRUE (1)
    finally:
        connection.close()

# Fonction pour valider le code de licence
def validate_licence():
    code_saisi = licence_entry.get()

    connection = connect_to_db()
    if connection is None:
        messagebox.showinfo("Connexion à la base de données", "L'application n'est pas connectée à la base de données.")
        return

    try:
        with connection.cursor() as cursor:
            query = "SELECT valeur_prevue FROM Licence LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()

            if result and result[0] == code_saisi:
                cursor.execute(
                    "UPDATE Licence SET valeur_saisie = %s, est_valide = TRUE WHERE valeur_prevue = %s",
                    (code_saisi, code_saisi)
                )
                connection.commit()
                messagebox.showinfo("Validation réussie", "Code de licence validé.")
                licence_window.destroy()
                show_login_window()  # Passer à la fenêtre d'authentification
            else:
                messagebox.showerror("Erreur", "Code de licence invalide.")
    finally:
        connection.close()

# Fonction pour afficher la fenêtre d'authentification
def show_login_window():
    global parent, username_entry, password_entry, login_button

    parent = tk.Tk()
    parent.title("Connexion sur   **Presta**(SGCE) ")
    parent.geometry("800x650")
    parent.resizable(0, 0)

    # Chargement de l'image
    image_path = "./images/presta1.png"  # Remplacez par le chemin de votre image
    image = Image.open(image_path)
    image = image.resize((500, 450), Image.BILINEAR)  # Redimensionnez l'image si nécessaire
    photo = ImageTk.PhotoImage(image)

    # Ajout de l'image
    image_label = tk.Label(parent, image=photo)
    image_label.image = photo  # Empêche l'image d'être garbage collected
    image_label.place(x=170, y=-25)

    label_entete = tk.Label(parent, text="AUTHENTIFICATION", font=("Shrikhand", 24, "bold"), fg="#5ca9bb")
    label_entete.place(x=270, y=350)

    # Création des champs de formulaire
    username_label = tk.Label(parent, text="Nom d'Utilisateur :", font=("Shrikhand", 10, "bold"))
    username_label.place(x=90, y=400)

    username_entry = tk.Entry(parent)
    username_entry.place(width=370, height=30, x=260, y=400)

    password_label = tk.Label(parent, text="Mot de Passe :", font=("Shrikhand", 10, "bold"))
    password_label.place(x=120, y=490)

    password_entry = tk.Entry(parent, show="*")
    password_entry.place(width=370, height=30, x=260, y=490)

    # Bouton de connexion
    login_button = tk.Button(parent, text="Login", command=validate_login)
    login_button.config(font=("Shrikhand", 12, "bold"))
    login_button.place(width=200, height=30, x=340, y=585)

    change_button_color()

    parent.mainloop()

# Fonction pour valider les identifiants de connexion
def validate_login():
    global user_info

    user_id = username_entry.get()
    password = password_entry.get()

    connection = connect_to_db()
    if connection is None:
        messagebox.showinfo("Connexion à la base de données", "L'application n'est pas connectée à la base de données.")
        return

    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM admin WHERE nom=%s AND mot_de_passe=%s"
            cursor.execute(query, (user_id, password))
            result = cursor.fetchone()

            if result:
                user_info = {
                    "admin_id": result[0],
                    "nom": result[1],
                    "prenom": result[2],
                    "email": result[3],
                    "date_creation": result[6]
                }
                messagebox.showinfo("Connexion réussie!", f"Bienvenue {user_info['prenom']} {user_info['nom']}")
                parent.destroy()
                import HomeDashAdmin
                HomeDashAdmin.open_welcome_window(user_info)
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects")
    finally:
        connection.close()

# Fonction pour changer la couleur du bouton
def change_button_color():
    new_color = "#5ca9bb"
    login_button.config(bg=new_color)

# Lancement de l'application
if is_licence_valid():
    show_login_window()
else:
    # Fenêtre pour entrer le code de licence
    licence_window = tk.Tk()
    licence_window.title("Validation de la Licence")
    licence_window.geometry("400x200")

    licence_label = tk.Label(licence_window, text="Entrez le code de licence :", font=("Helvetica", 12))
    licence_label.pack(pady=10)

    licence_entry = tk.Entry(licence_window, font=("Helvetica", 12))
    licence_entry.pack(pady=5)

    validate_button = tk.Button(licence_window, text="Valider", font=("Helvetica", 12, "bold"), command=validate_licence)
    validate_button.pack(pady=10)

    licence_window.mainloop()
