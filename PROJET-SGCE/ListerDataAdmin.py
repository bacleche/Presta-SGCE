import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import qrcode
from PIL import Image, ImageTk

import subprocess

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Variable globale pour le nom de l'utilisateur connecté
current_user_name = "Admin"  # Valeur par défaut

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



def get_classes():
    connection = get_db_connection()
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
    connection = get_db_connection()
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
    connection = get_db_connection()
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
    connection = get_db_connection()
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




def show_section(section):
    global global_tree
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    if section == "Données":
        columns = ("ID", "Nom", "Prénom", "date de Naissance", "Classe", "Niveau", "Filière", "Option")
        global_tree = ttk.Treeview(content_frame, columns=columns, show="headings")
        
        
        
        for col in columns:
            global_tree.heading(col, text=col)
            global_tree.column(col, width=100)
            
        scrollbar_x = ttk.Scrollbar(content_frame, orient=tk.HORIZONTAL, command=global_tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        global_tree.configure(xscrollcommand=scrollbar_x.set)

        scrollbar_y = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=global_tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        global_tree.configure(yscrollcommand=scrollbar_y.set)
        # Placement correct de la barre de défilement
     
        
        
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id, nom, prenom, date_frequentation, classe, niveau, filiere , options FROM etudiant")
                    data = cursor.fetchall()
                    for item in data:
                        global_tree.insert("", tk.END, values=item)
            except pymysql.MySQLError as e:
                messagebox.showerror("Erreur de requête", f"Erreur lors de la récupération des données: {e}")
            finally:
                connection.close()
        
        # global_tree.pack(fill="both", expand=True, padx=20, pady=20)
        global_tree.pack(fill="both", expand=True, padx=20, pady=(20, 0))
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        action_frame = tk.Frame(content_frame)
        action_frame.pack(pady=10)

        edit_button = tk.Button(action_frame, text="Modifier", font="Shrikhand" ,command=lambda: edit_item(global_tree))
        edit_button.pack(side="left", padx=5)

        delete_button = tk.Button(action_frame, text="Supprimer", font="Shrikhand", command=lambda: delete_item(global_tree))
        delete_button.pack(side="left", padx=5)

        view_button = tk.Button(action_frame, text="Visualiser", font="Shrikhand", command=lambda: view_item(global_tree))
        view_button.pack(side="left", padx=5)
    
    elif section == "Statistique":
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT date, COUNT(*) FROM presence WHERE statut = 'Présent' GROUP BY date ORDER BY date")
                    data = cursor.fetchall()
            except pymysql.MySQLError as e:
                messagebox.showerror("Erreur de requête", f"Erreur lors de la récupération des statistiques: {e}")
                return
            finally:
                connection.close()

        # Extraire les données
        dates, effectifs = zip(*data) if data else ([], [])

        # Création du graphique
        fig, ax = plt.subplots(figsize=(8, 5))
        
        ax.plot(dates, effectifs, marker='o', linestyle='-', color='b', label="Présences")
        
        ax.set_xlabel("Date")
        ax.set_ylabel("Nombre d'étudiants présents")
        ax.set_title("Présence journalière des étudiants")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)

        # Rotation des dates pour meilleure lisibilité
        plt.xticks(rotation=45)

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        canvas.draw()


    elif section == "Accueil":
        label = tk.Label(content_frame, text="Bienvenue sur la page d'accueil !", font=("Shrikhand", 12))
        label.pack(padx=20, pady=20)
        
    elif section == "Profil":
        info_frame = tk.Frame(content_frame, bg="white")
        info_frame.pack(padx=20, pady=20)

        tk.Label(info_frame, text="Nom:", font=("Shrikhand", 12)).grid(row=0, column=0, sticky="w")
        tk.Label(info_frame, text="", font=("Shrikhand", 12, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(info_frame, text="Prénom:", font=("Shrikhand", 12)).grid(row=1, column=0, sticky="w")
        tk.Label(info_frame, text="", font=("Shrikhand", 12, "bold")).grid(row=1, column=1, sticky="w")
        tk.Label(info_frame, text="date de naissance:", font=("Shrikhand", 12)).grid(row=2, column=0, sticky="w")
        tk.Label(info_frame, text="", font=("Shrikhand", 12, "bold")).grid(row=2, column=1, sticky="w")
        
    elif section == "Paramètres":
        label = tk.Label(content_frame, text="Voici les paramètres.", font=("Shrikhand", 12))
        label.pack(padx=20, pady=20)
        
    elif section == "Déconnexion":
        root.destroy()



# def create_item():
#     create_window = tk.Toplevel(root)
#     create_window.title("Créer un nouvel élément")
    
#     tk.Label(create_window, text="Nom:").grid(row=0, column=0, padx=10, pady=10)
#     nom_entry = tk.Entry(create_window)
#     nom_entry.grid(row=0, column=1, padx=10, pady=10)
    
#     tk.Label(create_window, text="Prénom:").grid(row=1, column=0, padx=10, pady=10)
#     prenom_entry = tk.Entry(create_window)
#     prenom_entry.grid(row=1, column=1, padx=10, pady=10)
    
#     tk.Label(create_window, text="date de naissance:").grid(row=2, column=0, padx=10, pady=10)
#     dob_entry = tk.Entry(create_window)
#     dob_entry.grid(row=2, column=1, padx=10, pady=10)
    
#     def save_new_item():
#         connection = get_db_connection()
#         if connection:
#             try:
#                 with connection.cursor() as cursor:
#                     sql = "INSERT INTO employe (nom, prenom, date_embauche) VALUES (%s, %s, %s)"
#                     cursor.execute(sql, (nom_entry.get(), prenom_entry.get(), dob_entry.get()))
#                     connection.commit()
#                     print(f"Élément créé: {nom_entry.get()}, {prenom_entry.get()}, {dob_entry.get()}")
#             except pymysql.MySQLError as e:
#                 messagebox.showerror("Erreur de sauvegarde", f"Erreur lors de la sauvegarde de l'élément: {e}")
#             finally:
#                 connection.close()
        
#         create_window.destroy()
    
#     save_button = tk.Button(create_window, text="Sauvegarder", command=save_new_item)
#     save_button.grid(row=3, column=0, columnspan=2, pady=10)


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


def qr_img_to_base64(img):
    """Convertit une image QR Code en une chaîne Base64."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

import base64
import io

from pymysql import Error


def edit_item(tree):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        values = item["values"]
        
        edit_window = tk.Toplevel(root)
        edit_window.title("Modifier l'élément")
        # edit_window.resizable(0, 0)
        
        # Création des champs de saisie
        tk.Label(edit_window, text="ID:").grid(row=0, column=0, padx=10, pady=10)
        id_entry = tk.Entry(edit_window)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        id_entry.insert(0, values[0])
        id_entry.config(state='readonly')
        
        tk.Label(edit_window, text="Nom:").grid(row=1, column=0, padx=10, pady=10)
        nom_entry = tk.Entry(edit_window)
        nom_entry.grid(row=1, column=1, padx=10, pady=10)
        nom_entry.insert(0, values[1])
        
        tk.Label(edit_window, text="Prénom:").grid(row=2, column=0, padx=10, pady=10)
        prenom_entry = tk.Entry(edit_window)
        prenom_entry.grid(row=2, column=1, padx=10, pady=10)
        prenom_entry.insert(0, values[2])
        
        tk.Label(edit_window, text="Date de Naissance:").grid(row=3, column=0, padx=10, pady=10)
        dob_entry = tk.Entry(edit_window)
        dob_entry.grid(row=3, column=1, padx=10, pady=10)
        dob_entry.insert(0, values[3])
        
        
        label_classe = tk.Label(edit_window, text="Classe:", font="Arial")
        label_classe.grid(row=0, column=2, sticky=tk.W)
        combobox_classe = ttk.Combobox(edit_window, values=get_classes())  # Créez la Combobox ici
        combobox_classe.grid(row=0, column=2, padx=95, pady=10)
        combobox_classe.insert(0, values[4])
        
        
        label_niveau = tk.Label(edit_window, text="Niveau:", font="Arial")
        label_niveau.grid(row=1, column=2, sticky=tk.W)
        combobox_niveau = ttk.Combobox(edit_window, values=get_niveaux())  # Créez la Combobox ici
        combobox_niveau.grid(row=1, column=2, padx=95, pady=10)
        combobox_niveau.insert(0, values[5])
        
        
        label_filiere = tk.Label(edit_window, text="Filière:", font="Arial")
        label_filiere.grid(row=2, column=2, sticky=tk.W)
        combobox_filiere = ttk.Combobox(edit_window, values=get_filieres())  # Créez la Combobox ici
        combobox_filiere.grid(row=2, column=2, padx=95, pady=10)
        combobox_filiere.insert(0, values[6])
        
        
        label_option = tk.Label(edit_window, text="Option:", font="Arial")
        label_option.grid(row=3, column=2, sticky=tk.W)
        combobox_option = ttk.Combobox(edit_window, values=get_Options())  # Créez la Combobox ici
        combobox_option.grid(row=3, column=2, padx=95, pady=10)
        combobox_option.insert(0, values[7])
        

        # Fonction pour générer et afficher le QR Code
        def update_qr_code():
            qr_data = f"{id_entry.get()}  {nom_entry.get()} {prenom_entry.get()}  {combobox_classe.get()}  {combobox_niveau.get()} {combobox_filiere.get()}  {combobox_option.get()}"
            qr_code_image = generate_qr_code(qr_data).convert("RGB")  # Assurer le bon format
            qr_code_photo = ImageTk.PhotoImage(qr_code_image)
            qr_code_label.config(image=qr_code_photo)
            qr_code_label.image = qr_code_photo 

        # Affichage du QR Code
        qr_code_label = tk.Label(edit_window)
        # qr_code_label.grid(row=4, column=0, columnspan=2, pady=10)
        qr_code_label.grid(row=4, column=0, columnspan=2, pady=10, padx=80)

        update_qr_code()  # Affichage initial du QR Code

        def save_changes():
            connection = get_db_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        
                        cursor.execute("SELECT classe_id FROM Classe WHERE libelle = %s", (combobox_classe.get(),))
                        classe_id_row = cursor.fetchone()
                        if classe_id_row:
                            classe_id = classe_id_row[0]
                        else:
                            print("Classe sélectionnée invalide")
                            print(combobox_classe.get())
                            return

                        cursor.execute("SELECT niveau_id FROM Niveau WHERE libelle = %s", (combobox_niveau.get(),))
                        niveau_id_row = cursor.fetchone()
                        if niveau_id_row:
                            niveau_id = niveau_id_row[0]
                        else:
                            print("Niveau sélectionné invalide")
                            print(combobox_niveau.get())
                            
                            return

                        cursor.execute("SELECT options_id FROM Options WHERE libelle = %s", (combobox_option.get(),))
                        option_id_row = cursor.fetchone()
                        if option_id_row:
                            option_id = option_id_row[0]
                        else:
                            print("Option sélectionnée invalide")
                            print(combobox_option.get())
                            
                            return

                        cursor.execute("SELECT filiere_id FROM Filiere WHERE libelle = %s", (combobox_filiere.get(),))
                        filiere_id_row = cursor.fetchone()
                        if filiere_id_row:
                            filiere_id = filiere_id_row[0]
                        else:
                            print("Filière sélectionnée invalide")
                            print(combobox_filiere.get())
                            
                            return

                        sql = """UPDATE etudiant 
                                SET nom=%s, prenom=%s, date_frequentation=%s, 
                                    `classe`=%s, `niveau`=%s, `filiere`=%s, `options`=%s  
                                WHERE id=%s"""
                        cursor.execute(sql, (nom_entry.get(), prenom_entry.get(), dob_entry.get(), 
                                            classe_id, niveau_id, filiere_id, option_id, values[0]))

                        connection.commit()

                        # Générer le QR Code mis à jour
                        qr_data = f"ID: {values[0]}, Nom: {nom_entry.get()}, Prénom: {prenom_entry.get()}, Niveau: {combobox_niveau.get()} , Classe: {combobox_classe.get() },  Filière: {combobox_filiere.get()} ,  Option: {combobox_option.get()}"
                        new_qr_code_image = generate_qr_code(qr_data)
                        new_qr_code_base64 = qr_img_to_base64(new_qr_code_image)

                        # Mettre à jour le QR Code en Base64 dans la base de données
                        sql_update_qr = "UPDATE etudiant SET qr_code=%s WHERE id=%s"
                        cursor.execute(sql_update_qr, (new_qr_code_base64, values[0]))
                        connection.commit()

                except pymysql.MySQLError as e:
                    messagebox.showerror("Erreur de sauvegarde", f"Erreur lors de la sauvegarde des modifications: {e}")
                finally:
                    connection.close()

            # Mettre à jour l'élément dans l'interface
            tree.item(selected_item, values=(
                values[0], nom_entry.get(), prenom_entry.get(), dob_entry.get(),
                combobox_classe.get(), combobox_niveau.get(), combobox_filiere.get(), combobox_option.get()
            ))

            edit_window.destroy()




        # Bouton pour sauvegarder les modifications
        save_button = tk.Button(edit_window, text="Sauvegarder", command=save_changes)
        save_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Mettre à jour le QR code lorsque les champs changent
        for entry in [nom_entry, prenom_entry, dob_entry]:
            entry.bind("<KeyRelease>", lambda event: update_qr_code())
        
    else:
        messagebox.showwarning("Aucun élément sélectionné", "Veuillez sélectionner un élément à modifier.")



def delete_item(tree):
    selected_item = tree.selection()
    if selected_item:
        response = messagebox.askyesno("Confirmer la suppression", "Êtes-vous sûr de vouloir supprimer cet élément ?")
        if response:
            item = tree.item(selected_item)
            item_id = item["values"][0]
            
            connection = get_db_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = "DELETE FROM etudiant WHERE id=%s"
                        cursor.execute(sql, (item_id,))
                        connection.commit()
                        print("Élément supprimé")
                except pymysql.MySQLError as e:
                    messagebox.showerror("Erreur de suppression", f"Erreur lors de la suppression de l'élément: {e}")
                finally:
                    connection.close()
            
            tree.delete(selected_item)
    else:
        messagebox.showwarning("Aucun élément sélectionné", "Veuillez sélectionner un élément à supprimer.")

def view_item(tree):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        values = item["values"]
        
        view_window = tk.Toplevel(root)
        view_window.title("Visualiser l'élément")
        
        tk.Label(view_window, text="ID:", font=("Shrikhand", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(view_window, text=values[0], font=("Shrikhand", 12)).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        tk.Label(view_window, text="Nom:", font=("Shrikhand", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Label(view_window, text=values[1], font=("Shrikhand", 12)).grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        tk.Label(view_window, text="Prénom:", font=("Shrikhand", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Label(view_window, text=values[2], font=("Shrikhand", 12)).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        tk.Label(view_window, text="date de Naissance:", font=("Shrikhand", 12, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        tk.Label(view_window, text=values[3], font=("Shrikhand", 12)).grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        close_button = tk.Button(view_window, text="Fermer", font="Shrikhand" , command=view_window.destroy)
        close_button.grid(row=4, column=0, columnspan=2, pady=10)
    else:
        messagebox.showwarning("Aucun élément sélectionné", "Veuillez sélectionner un élément à visualiser.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Liste **Presta**")
root.geometry("1000x600")
# root.resizable(0, 0)

# Cadre pour le titre
header_frame = tk.Frame(root, bg="#5ca9bb", height=100)
header_frame.pack(fill="x")

# Titre de l'en-tête
header_label = tk.Label(header_frame, text="Dashboard Home", fg="white" ,font=("Shrikhand", 24), bg="#5ca9bb")
header_label.pack(pady=10, side="left", padx=20)

# Étiquette pour le nom de l'utilisateur
user_label = tk.Label(header_frame, text=f"Connecté en tant que : {current_user_name}", font=("Shrikhand", 12), fg="white", bg="#5ca9bb")
user_label.pack(pady=10, side="right", padx=20)

# Cadre pour le contenu principal
content_frame = tk.Frame(root, bg="white", width=700, height=500)
content_frame.pack(fill="both", expand=True, side="left", padx=80, pady=80)

# Cadre pour le contenu latéral (sidebar)
sidebar_frame = tk.Frame(root, bg="lightgray", width=150)
sidebar_frame.pack(fill="y", side="right", padx=10, pady=10)

# Fonction pour activer le bouton "Lire"
# def enable_read_button():
#     read_button.config(state=tk.NORMAL)

# Boutons pour actions sur les employés (sidebar)
# employee_buttons = ["Créer", "Lire"]

# for i in range(0, len(employee_buttons), 2):
#     button_frame = tk.Frame(sidebar_frame)
#     button_frame.pack(pady=5, fill="x")

#     button1 = tk.Button(button_frame, text=employee_buttons[i], width=15, height=2, font=("Shrikhand", 12), command=lambda text=employee_buttons[i]: show_section(text))
#     button1.pack(side="left", padx=5, pady=5)
    
#     if employee_buttons[i] == "Lire":
#         read_button = button1
#         read_button.config(state=tk.DISABLED)

#     if i + 1 < len(employee_buttons):
#         button2 = tk.Button(button_frame, text=employee_buttons[i + 1], width=15, height=2, font=("Shrikhand", 12), command=lambda text=employee_buttons[i + 1]: show_section(text))
#         button2.pack(side="left", padx=5, pady=5)
        
#         if employee_buttons[i + 1] == "Lire":
#             read_button = button2
#             read_button.config(state=tk.DISABLED)
def ouvrir_creer_employe():
        subprocess.Popen(["python", "RegisterDataAdmin.py"])


employee_buttons = ["Créer", "Lire"]

for i in range(0, len(employee_buttons), 2):
    button_frame = tk.Frame(sidebar_frame)
    button_frame.pack(pady=5, fill="x")

    button1_command = ouvrir_creer_employe if employee_buttons[i] == "Créer" else lambda text=employee_buttons[i]: show_section(text)
    button1 = tk.Button(button_frame, text=employee_buttons[i], width=15, height=2, font=("Shrikhand", 12), command=button1_command)
    button1.pack(side="left", padx=5, pady=5)
    
    if employee_buttons[i] == "Lire":
        button1.config(state=tk.DISABLED)
#         read_button.config(state=tk.DISABLED)
        

    if i + 1 < len(employee_buttons):
        button2_command = ouvrir_creer_employe if employee_buttons[i + 1] == "Créer" else lambda text=employee_buttons[i + 1]: show_section(text)
        button2 = tk.Button(button_frame, text=employee_buttons[i + 1], width=15, height=2, font=("Shrikhand", 12), command=button2_command)
        button2.pack(side="left", padx=5, pady=5)
        
        if employee_buttons[i + 1] == "Lire":
            button2.config(state=tk.DISABLED)

# Boutons de navigation principaux
nav_buttons = ["Données", "Statistique"]

for nav_button_text in nav_buttons:
    button = tk.Button(sidebar_frame, text=nav_button_text, width=15, height=2,
                       font=("Shrikhand", 12), command=lambda text=nav_button_text: show_section(text))
    button.pack(pady=5, fill="x")

# Afficher la section par défaut
show_section("Données")

root.mainloop()
