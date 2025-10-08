import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from tkinter import messagebox
import pymysql
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


def open_welcome_window(user_info):
    # Création de la fenêtre d'accueil
    root = tk.Tk()
    root.title("Dashboard Home")
    root.geometry("800x600")

    # Cadre pour le titre
    header_frame = tk.Frame(root, bg="#5ca9bb", height=100)
    header_frame.pack(fill="x")

    # Titre de l'en-tête
    header_label = tk.Label(header_frame, text="Dashboard Home", font=("Shrikhand", 24), fg="white", bg="#5ca9bb")
    header_label.pack(pady=30)

    # Cadre pour le contenu principal
    content_frame = tk.Frame(root, bg="#5ca9bb", width=300, height=400)
    content_frame.pack(fill="both", expand=True, side="left", padx=80, pady=80)

    # Cadre pour le contenu latéral (sidebar)
    sidebar_frame = tk.Frame(root, bg="lightgray", width=150)
    sidebar_frame.pack(fill="y", side="right", padx=10, pady=10)

    bas_frame = tk.Frame(sidebar_frame, bg="lightgray", width=150)
    bas_frame.pack(fill="x", side="bottom", padx=50, pady=50)

    # Fonctions pour ouvrir d'autres fichiers .py
    def ouvrir_creer_employe():
        subprocess.Popen(["python", "RegisterDataAdmin.py"])

    def ouvrir_lire_employe():
        subprocess.Popen(["python", "ListerDataAdmin.py"])

    def ouvrir_mettre_a_jour_employe():
        subprocess.Popen(["python", "mettre_a_jour_employe.py"])
        
    def ouvrir_parametrageN_C():
        subprocess.Popen(["python", "ParametrageN_C.py"])

    def ouvrir_parametrageF_O():
        subprocess.Popen(["python", "ParametrageF_O.py"])
        
    def ouverture_presence():
        subprocess.Popen(["python", "ListePresence.py"])
        
    def initialiser_ecole():
        subprocess.Popen(["python", "ecole.py"])


    # Boutons pour actions sur les employés (sidebar)
    employee_buttons = {
        "Créer": ouvrir_creer_employe,
        "Lire": ouvrir_lire_employe,
        "visualier les presences": ouverture_presence,
        "Parametrage Niveau & Classe": ouvrir_parametrageN_C,
        "Parametrage Filière & Option": ouvrir_parametrageF_O,
        "Initialiser Etablissement": initialiser_ecole
        
        
    }

    for text, command in employee_buttons.items():
        button_frame = tk.Frame(sidebar_frame)
        button_frame.pack(pady=5, fill="x")

        button = tk.Button(button_frame, text=text, width=150, height=2, font=("Shrikhand", 12), command=command)
        button.pack(side="left", padx=5, pady=5)

    # Boutons de navigation principaux
    nav_buttons = ["Accueil", "Profil", "Déconnexion"]

    def show_section(section):
        # Efface le contenu précédent
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        # Affiche le contenu de la section sélectionnée
        if section == "Accueil":
            label = tk.Label(content_frame, text=f"{user_info['prenom']} {user_info['nom']}!", bg="#5ca9bb" ,font=("Shrikhand", 12))
            label.pack(padx=20, pady=20)

            # Chargement de l'image
            image_path = "./images/presta1.png"  # Remplacez par le chemin de votre image
            image = Image.open(image_path)
            image = image.resize((500, 450), Image.BILINEAR)  # Redimensionnez l'image si nécessaire
            photo = ImageTk.PhotoImage(image)

            # Ajout de l'image à l'aide d'un label
            image_label = tk.Label(content_frame, image=photo)
            image_label.image = photo  # Garder une référence à l'objet PhotoImage
            image_label.pack(padx=20, pady=20)
            
        elif section == "Profil":
            # Informations personnelles
            info_frame = tk.Frame(content_frame, bg="white")
            info_frame.pack(padx=20, pady=20)

            # Exemple de données (à remplacer par les vraies données)
            nom = f"{user_info['nom']}"
            prenom = f"{user_info['prenom']}"
            email = f"{user_info['email']}"
            Date_creation = f"{user_info['date_creation']}"
            

            # Labels pour les informations personnelles
            tk.Label(info_frame, text="Nom:", bg="white",font=("Shrikhand", 12)).grid(row=0, column=0, sticky="w")
            tk.Label(info_frame, text=nom, bg="white",font=("Shrikhand", 12, "bold")).grid(row=0, column=1, sticky="w")
            tk.Label(info_frame, text="Prénom:", bg="white",font=("Shrikhand", 12)).grid(row=1, column=0, sticky="w")
            tk.Label(info_frame, text=prenom,bg="white", font=("Shrikhand", 12, "bold")).grid(row=1, column=1, sticky="w")
            
            tk.Label(info_frame, text="Email:", bg="white",font=("Shrikhand", 12)).grid(row=2, column=0, sticky="w")
            tk.Label(info_frame, text=email, bg="white",font=("Shrikhand", 12, "bold")).grid(row=2, column=1, sticky="w")
            
            tk.Label(info_frame, text="Date de creation du profil:", bg="white",font=("Shrikhand", 12)).grid(row=3, column=0, sticky="w")
            tk.Label(info_frame, text=Date_creation, bg="white",font=("Shrikhand", 12, "bold")).grid(row=3, column=1, sticky="w")
            
            
             # Bouton "Modifier Profil"
            btn_modify = tk.Button(info_frame, text="Modifier Profil", font=("Shrikhand", 12), command=open_modify_profile_window)
            btn_modify.grid(row=4, column=0, columnspan=2, pady=10)

        
        
        # elif section == "Paramètres":
        #     label = tk.Label(content_frame, text="Voici les paramètres.", font=("Shrikhand", 12))
        #     label.pack(padx=20, pady=20)
            
        elif section == "Déconnexion":
            root.destroy()
            
    def open_modify_profile_window():
        modify_window = tk.Toplevel(root)
        modify_window.title("Modifier le Profil **Presta**")
        modify_window.geometry("300x300")
        modify_window.resizable(0, 0)
        

        # Pré-remplir les champs avec les informations actuelles de l'utilisateur
        nom_var = tk.StringVar(value=user_info['nom'])
        prenom_var = tk.StringVar(value=user_info['prenom'])
        email_var = tk.StringVar(value=user_info['email'])

        tk.Label(modify_window, text="Nom:", font=("Shrikhand", 12)).pack(pady=5)
        nom_entry = tk.Entry(modify_window, textvariable=nom_var, font=("Shrikhand", 12))
        nom_entry.pack(pady=5)

        tk.Label(modify_window, text="Prénom:", font=("Shrikhand", 12)).pack(pady=5)
        prenom_entry = tk.Entry(modify_window, textvariable=prenom_var, font=("Shrikhand", 12))
        prenom_entry.pack(pady=5)

        tk.Label(modify_window, text="Email:", font=("Shrikhand", 12)).pack(pady=5)
        email_entry = tk.Entry(modify_window, textvariable=email_var, font=("Shrikhand", 12))
        email_entry.pack(pady=5)

        def save_profile():
            # Récupérer les nouvelles valeurs
            new_nom = nom_entry.get().strip()
            new_prenom = prenom_entry.get().strip()
            new_email = email_entry.get().strip()

            # Validation des entrées
            if not new_nom or not new_prenom or not new_email:
                messagebox.showwarning("Attention", "Tous les champs doivent être remplis.")
                return

            id = user_info['admin_id']
            print(id)
            try:
                connection = connect_to_db()
                if connection is None:
                    raise Exception("La connexion à la base de données a échoué.")

                with connection.cursor() as cursor:
                    # Requête SQL pour mettre à jour le profil
                    query = "UPDATE admin SET nom = %s, prenom = %s, email = %s WHERE admin_id = %s"
                    cursor.execute(query, (new_nom, new_prenom, new_email, id))

                # Valider la transaction
                connection.commit()
                messagebox.showinfo("Succès", "Profil mis à jour avec succès")
                modify_window.destroy()

                # Mettre à jour les informations dans user_info et rafraîchir l'affichage
                user_info['nom'] = new_nom
                user_info['prenom'] = new_prenom
                user_info['email'] = new_email
                show_section("Profil")

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du profil : {e}")

            finally:
                if connection:
                    connection.close()

        # Bouton "Sauvegarder"
        btn_save = tk.Button(modify_window, text="Sauvegarder", font=("Shrikhand", 12), command=save_profile)
        btn_save.pack(pady=20)

    # Boutons de navigation principaux
    for nav_button_text in nav_buttons:
        button = tk.Button(bas_frame, text=nav_button_text, width=15, height=2,
                           font=("Shrikhand", 12), command=lambda text=nav_button_text: show_section(text))
        button.pack(side="left", padx=10, pady=10)

    # Afficher la section par défaut
    show_section("Accueil")

    root.mainloop()

# open_welcome_window()
