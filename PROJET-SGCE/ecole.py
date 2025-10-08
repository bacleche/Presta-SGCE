import tkinter as tk
from tkinter import filedialog, messagebox
import pymysql

def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',  # Remplace par ton utilisateur MySQL
            password='',  # Remplace par ton mot de passe MySQL
            database='SGCE'
        )
        return connection
    except pymysql.MySQLError as e:
        messagebox.showerror("Erreur", f"Erreur de connexion MySQL: {e}")
        return None

def choisir_image():
    filepath = filedialog.askopenfilename(title="Choisir une image",  filetypes=[("Tous les fichiers", "*.*")]
)
    if filepath:
        entry_logo.delete(0, tk.END)
        entry_logo.insert(0, filepath)

def enregistrer_ecole():
    libelle = entry_libelle.get()
    logo = entry_logo.get()
    email = entry_email.get()
    telephone = entry_telephone.get()
    
    if not libelle or not email or not telephone:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
        return
    
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO ecole (libelle, logo, email, telephone) VALUES (%s, %s, %s, %s)",
                               (libelle, logo, email, telephone))
                conn.commit()
            messagebox.showinfo("Succès", "École enregistrée avec succès! , Nombre :(1x)")
            clear_fields()
        finally:
            conn.close()

def supprimer_ecole():
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE ecole")
                conn.commit()
            messagebox.showinfo("Succès", "Votre etablissement a été supprimée de la base !")
            clear_fields()
        finally:
            conn.close()

def clear_fields():
    entry_libelle.delete(0, tk.END)
    entry_logo.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telephone.delete(0, tk.END)

# Interface Tkinter
root = tk.Tk()
root.title("Creation etablissement **Presta**")
root.geometry("800x350")
root.resizable(0,0)

# Libellé
label_libelle = tk.Label(root, text="Libellé de l'école:",font=("Shrikhand", 12))
label_libelle.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_libelle = tk.Entry(root, width=40)
entry_libelle.grid(row=0, column=1, padx=10, pady=5)

# Logo
label_logo = tk.Label(root, text="Logo:", font=("Shrikhand", 12))
label_logo.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_logo = tk.Entry(root, width=30)
entry_logo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
button_choisir = tk.Button(root, text="Choisir Image", command=choisir_image, font=("Shrikhand", 12))
button_choisir.grid(row=1, column=2, padx=5, pady=5)

# Email
label_email = tk.Label(root, text="Email:", font=("Shrikhand", 12))
label_email.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_email = tk.Entry(root, width=40)
entry_email.grid(row=2, column=1, padx=10, pady=5)

# Téléphone
label_telephone = tk.Label(root, text="Téléphone:", font=("Shrikhand", 12))
label_telephone.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_telephone = tk.Entry(root, width=40)
entry_telephone.grid(row=3, column=1, padx=10, pady=5)

# Boutons
button_enregistrer = tk.Button(root, text="Enregistrer", command=enregistrer_ecole, font=("Shrikhand", 12))
button_enregistrer.grid(row=4, column=0, columnspan=2, pady=10)

button_supprimer = tk.Button(root, text="Supprimer", command=supprimer_ecole, fg="red", font=("Shrikhand", 12))
button_supprimer.grid(row=5, column=0, columnspan=2, pady=10)

# Démarrer l'interface
root.mainloop()
