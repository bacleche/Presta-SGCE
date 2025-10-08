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

# Fonction pour ajouter une entrée dans le tableau Niveau
def add_to_niveau():
    value = entry_niveau.get()
    if value:
        insert_data("Niveau", "NIV", value)
        load_niveau_data()
        entry_niveau.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrée manquante", "Veuillez entrer un libellé pour le Niveau.")

# Fonction pour ajouter une entrée dans le tableau Classe
def add_to_classe():
    value = entry_classe.get()
    if value:
        insert_data("Classe", "CL", value)
        load_classe_data()
        entry_classe.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrée manquante", "Veuillez entrer un libellé pour la Classe.")


# Fonction pour charger les données dans le tableau Niveau
def load_niveau_data():
    for item in tree_niveau.get_children():
        tree_niveau.delete(item)
    rows = fetch_data("Niveau")
    for row in rows:
        tree_niveau.insert("", tk.END, values=row)

# Fonction pour charger les données dans le tableau Classe
def load_classe_data():
    for item in tree_classe.get_children():
        tree_classe.delete(item)
    rows = fetch_data("Classe")
    for row in rows:
        tree_classe.insert("", tk.END, values=row)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface avec Niveau, Classe **Presta**")
root.geometry("1000x600")
root.configure(bg="#f0f0f0")

# Style pour les sections
frame_style = {"bg": "#e6e6e6", "bd": 2, "relief": "groove", "padx": 10, "pady": 10}
label_style = {"bg": "#e6e6e6", "fg": "#333", "font": ("Shrikhand", 12)}
entry_style = {"font": ("Shrikhand", 12)}

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

# Frame pour le formulaire Niveau
frame_niveau = tk.Frame(root, **frame_style)
frame_niveau.pack(pady=15, padx=15, fill="x")

label_niveau = tk.Label(frame_niveau, text="Formulaire Niveau :", **label_style)
label_niveau.grid(row=0, column=0, padx=5)

entry_niveau = tk.Entry(frame_niveau, width=30, **entry_style)
entry_niveau.grid(row=0, column=1, padx=5)

button_niveau = tk.Button(frame_niveau, text="Ajouter",font="Shrikhand", command=add_to_niveau)
button_niveau.grid(row=0, column=2, padx=5)

# Tableau Niveau
tree_niveau = setup_treeview(root, ["ID", "Libellé"], "Tableau Niveau")

# Frame pour le formulaire Classe
frame_classe = tk.Frame(root, **frame_style)
frame_classe.pack(pady=15, padx=15, fill="x")

label_classe = tk.Label(frame_classe, text="Formulaire Classe :", **label_style)
label_classe.grid(row=0, column=0, padx=5)

entry_classe = tk.Entry(frame_classe, width=30, **entry_style)
entry_classe.grid(row=0, column=1, padx=5)

button_classe = tk.Button(frame_classe, text="Ajouter", font="Shrikhand", command=add_to_classe)
button_classe.grid(row=0, column=2, padx=5)

# Tableau Classe
tree_classe = setup_treeview(root, ["ID", "Libellé"], "Tableau Classe")




# Charger les données au démarrage
load_niveau_data()
load_classe_data()

# Lancement de la fenêtre principale
root.mainloop()
