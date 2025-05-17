import json
import os
from models.automate import Automate

def ensure_directory(directory="Automates"):
    """S'assure que le répertoire existe."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_automate(automate, filename):
    """Sauvegarde un automate dans un fichier JSON."""
    ensure_directory()
    filepath = os.path.join("Automates", f"{filename}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(automate.to_dict(), f, indent=4)

def load_automate(filename):
    """Charge un automate depuis un fichier JSON."""
    filepath = os.path.join("Automates", f"{filename}.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Le fichier {filepath} n'existe pas.")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Automate.from_dict(data)

def list_saved_automates():
    """Retourne la liste des automates sauvegardés."""
    ensure_directory()
    return [f.replace(".json", "") for f in os.listdir("Automates") 
            if f.endswith(".json")]

def delete_automate(filename):
    """Supprime un automate sauvegardé."""
    filepath = os.path.join("Automates", f"{filename}.json")
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Erreur lors de la suppression: {str(e)}")
        return False 