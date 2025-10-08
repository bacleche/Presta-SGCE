import pyttsx3

def list_voices():
    # Initialiser le moteur de synthèse vocale
    engine = pyttsx3.init()
    
    # Obtenir les voix disponibles
    voices = engine.getProperty('voices')
    
    # Afficher les voix disponibles
    for voice in voices:
        print(f"ID: {voice.id}")
        print(f"Name: {voice.name}")
        print(f"Lang: {voice.languages}")
        print(f"Gender: {voice.gender}")
        print("-" * 40)

if __name__ == "__main__":
    list_voices()
