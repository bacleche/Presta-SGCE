import tkinter as tk
from tkinter import messagebox, ttk
import pymysql

# Connexion à la base de données MySQL
def connect_db():
    try:
        return pymysql.connect(
            host="localhost",    # Remplacez par votre hôte
            user="root",         # Remplacez par votre utilisateur
            password="",         # Remplacez par votre mot de passe
            database="SGCE"  # Remplacez par votre base de données
        )
    except pymysql.Error as e:
        messagebox.showerror("Erreur de connexion", f"Erreur lors de la connexion à la base de données : {str(e)}")
        return None

# Fonction pour générer le prochain ID dans un format spécifique (par exemple, NIV001, FIL001, CL001)
def generate_id(table, prefix):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = f"SELECT MAX({table}_id) FROM {table}"
                cursor.execute(query)
                last_id = cursor.fetchone()[0]
                if last_id:
                    # Extraire le numéro de l'ID actuel et l'incrémenter
                    num = int(last_id[len(prefix):]) + 1
                else:
                    num = 1
                return f"{prefix}{num:03d}"  # Format avec 3 chiffres, ex: NIV001
        except pymysql.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération de l'ID : {str(e)}")
        finally:
            conn.close()
    return None

# Fonction pour insérer des données dans la table MySQL
def insert_data(table, prefix, value):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                new_id = generate_id(table, prefix)
                query = f"INSERT INTO {table} ({table}_id, libelle) VALUES (%s, %s)"
                cursor.execute(query, (new_id, value))
                conn.commit()
        except pymysql.Error as e:
            messagebox.showerror("Erreur", f"Impossible d'insérer les données : {str(e)}")
        finally:
            conn.close()

# Fonction pour récupérer les données de la table MySQL
def fetch_data(table):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = f"SELECT {table}_id, libelle FROM {table}"
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.Error as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les données : {str(e)}")
            return []
        finally:
            conn.close()


# Fonction pour ajouter une entrée dans le tableau Filière
def add_to_filiere():
    value = entry_filiere.get()
    if value:
        insert_data("Filiere", "FIL", value)
        load_filiere_data()
        entry_filiere.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrée manquante", "Veuillez entrer un libellé pour la Filière.")

# Fonction pour ajouter une entrée dans le tableau Option
def add_to_option():
    value = entry_option.get()
    if value:
        insert_data("Options", "OPT", value)
        load_option_data()
        entry_option.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrée manquante", "Veuillez entrer un libellé pour l'Option.")

# Fonction pour charger les données dans le tableau Filière
def load_filiere_data():
    for item in tree_filiere.get_children():
        tree_filiere.delete(item)
    rows = fetch_data("Filiere")
    for row in rows:
        tree_filiere.insert("", tk.END, values=row)

# Fonction pour charger les données dans le tableau Option
def load_option_data():
    for item in tree_option.get_children():
        tree_option.delete(item)
    rows = fetch_data("Options")
    for row in rows:
        tree_option.insert("", tk.END, values=row)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface avec  Filière et Option **Presta**")
root.geometry("1000x600")
root.configure(bg="#f0f0f0")

# Style pour les sections
frame_style = {"bg": "#e6e6e6", "bd": 2, "relief": "groove", "padx": 10, "pady": 10}
label_style = {"bg": "#e6e6e6", "fg": "#333", "font": ("Shrikhand", 12)}
entry_style = {"font": ("Arial", 12)}

# Fonction pour configurer un tableau avec des colonnes et une scrollbar
def setup_treeview(parent, columns, title):
    label = tk.Label(root, text=title, font=("Shrikhand", 12, "bold"), bg="#f0f0f0")
    label.pack()

    frame = tk.Frame(parent)
    frame.pack(pady=10)

    tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
    tree.pack(side=tk.LEFT)

    tree.column("ID", width=100)
    tree.column("Libellé", width=500)

    for col in columns:
        tree.heading(col, text=col)

    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar_y.set)

    return tree


# Frame pour le formulaire Filière
frame_filiere = tk.Frame(root, **frame_style)
frame_filiere.pack(pady=15, padx=15, fill="x")

label_filiere = tk.Label(frame_filiere, text="Formulaire Filière :", **label_style)
label_filiere.grid(row=0, column=0, padx=5)

entry_filiere = tk.Entry(frame_filiere, width=30, **entry_style)
entry_filiere.grid(row=0, column=1, padx=5)

button_filiere = tk.Button(frame_filiere, font="Shrikhand", text="Ajouter", command=add_to_filiere)
button_filiere.grid(row=0, column=2, padx=5)

# Tableau Filière
tree_filiere = setup_treeview(root, ["ID", "Libellé"], "Tableau Filière")

# Frame pour le formulaire Option
frame_option = tk.Frame(root, **frame_style)
frame_option.pack(pady=15, padx=15, fill="x")

label_option = tk.Label(frame_option,  text="Formulaire Option :", **label_style)
label_option.grid(row=0, column=0, padx=5)

entry_option = tk.Entry(frame_option, width=30, **entry_style)
entry_option.grid(row=0, column=1, padx=5)

button_option = tk.Button(frame_option, font="Shrikhand", text="Ajouter", command=add_to_option)
button_option.grid(row=0, column=2, padx=5)

# Tableau Option
tree_option = setup_treeview(root, ["ID", "Libellé"], "Tableau Option")

# Charger les données au démarrage

load_filiere_data()
load_option_data()

# Lancement de la fenêtre principale
root.mainloop()
