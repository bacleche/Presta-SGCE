import cv2
from pyzbar.pyzbar import decode
import time
from datetime import datetime
import pymysql  # Pour se connecter à la base de données MySQL
import pyttsx3  # Synthèse vocale

# Initialiser la caméra
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Largeur de la caméra
cam.set(4, 480)  # Hauteur de la caméra

# Initialiser le moteur de synthèse vocale
engine = pyttsx3.init()

# Sélectionner une voix française et féminine
voices = engine.getProperty('voices')
selected_voice_id = None
for voice in voices:
    if 'fr' in voice.id and 'female' in voice.name.lower():
        selected_voice_id = voice.id
        break

if selected_voice_id:
    engine.setProperty('voice', selected_voice_id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Connexion à la base de données MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="SGCE"
)
cursor = db.cursor()

def speak(text):
    """Fonction pour faire parler la machine."""
    engine.say(text)
    engine.runAndWait()

# Variable pour suivre le dernier QR scanné et l'heure de ce scan
last_qr_data = None
last_scan_time = datetime.now()

try:
    while True:
        success, frame = cam.read()

        if not success:
            print("Erreur lors de la lecture de la caméra")
            break

        # Décoder le code QR
        decoded_barcodes = decode(frame)
        if decoded_barcodes:
            for barcode in decoded_barcodes:
                qr_data = barcode.data.decode('utf-8')
                scan_time = datetime.now()

                # Si le même QR code est scanné dans les 5 secondes, l'ignorer
                if qr_data == last_qr_data and (scan_time - last_scan_time).seconds < 5:
                    continue  # Ignorer ce scan car il est trop proche du précédent

                # Mettre à jour la dernière donnée scannée et l'heure du scan
                last_qr_data = qr_data
                last_scan_time = scan_time

                # Extraire les informations de l'étudiant à partir des données du QR code
                qr_values = qr_data.split(' ')  # Séparer les valeurs par le délimiteur '&'

                # Vérifiez que nous avons suffisamment de valeurs
                if len(qr_values) >= 3:
                    etudiant_id = qr_values[0].strip()  # Première valeur
                    prenom = qr_values[1].strip()        # Deuxième valeur (prénom)
                    classe = qr_values[5].strip()        # Troisième valeur (classe)
                else:
                    speak("Données QR invalides, veuillez vérifier la carte.")
                    print("Données QR invalides:", qr_data)
                    continue  # Passer à l'itération suivante de la boucle

                # Vérifier l'existence d'une entrée pour le même étudiant, date, et classe
                try:
                    date = scan_time.date()
                    sql_check = "SELECT * FROM presence WHERE etudiant_id = %s AND date = %s AND classe = %s"
                    cursor.execute(sql_check, (etudiant_id, date, classe))
                    result = cursor.fetchone()

                    if result:
                        speak("Présence déjà enregistrée pour aujourd'hui.")
                        print("Présence déjà enregistrée pour cet étudiant aujourd'hui.")
                        continue  # Passer à l'itération suivante de la boucle

                    # Insertion des données d'arrivée dans la table 'presences'
                    sql_insert = "INSERT INTO presence (etudiant_id, date, classe, heure_arrivee, statut) VALUES (%s, %s, %s, %s, %s)"
                    heure_arrivee = scan_time.time()
                    statut = "Présent"  # Vous pouvez ajuster le statut si nécessaire
                    cursor.execute(sql_insert, (etudiant_id, date, classe, heure_arrivee, statut))
                    db.commit()
                    print("Données insérées avec succès dans la base de données.")

                    speak("Présence enregistrée avec succès.")

                except pymysql.Error as e:
                    print(f"Erreur lors de l'insertion dans la base de données : {e}")
                    db.rollback()

                print("Données scannées:", qr_data)
                print("Heure de scan:", scan_time)

                # Après chaque scan, on évite les répétitions rapides
                time.sleep(1)

        # Afficher l'image capturée avec OpenCV
        cv2.imshow("OurQR_Code_Scanner", frame)

        # Quitter la boucle si la touche 'q' est appuyée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Programme interrompu par l'utilisateur")

finally:
    # Libérer la caméra et fermer toutes les fenêtres
    cam.release()
    cv2.destroyAllWindows()
    
    # Fermer la connexion à la base de données
    db.close()
