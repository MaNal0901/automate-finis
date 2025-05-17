import json
import os
from models.automate import Automate

AUTOMATES_DIR = "Automates/Automates"

def ensure_directory():
    """S'assure que le répertoire Automates existe."""
    if not os.path.exists(AUTOMATES_DIR):
        os.makedirs(AUTOMATES_DIR)

def save_automate(automate, filename):
    """Sauvegarde un automate dans un fichier JSON sous Automates/."""
    ensure_directory()
    filepath = os.path.join(AUTOMATES_DIR, f"{filename}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(automate.to_dict(), f, indent=4)
    print(f"✅ Automate sauvegardé sous : {filepath}")

def load_automate(filename):
    """Charge un automate depuis Automates/."""
    filepath = os.path.join(AUTOMATES_DIR, f"{filename}.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Le fichier {filepath} n'existe pas.")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Automate.from_dict(data)

def list_saved_automates():
    """Retourne la liste des automates sauvegardés (sans l'extension .json)."""
    ensure_directory()
    return [f.replace(".json", "") for f in os.listdir(AUTOMATES_DIR) if f.endswith(".json")]

# Test rapide du module (à exécuter uniquement si ce fichier est lancé directement)
if __name__ == "__main__":
    print("📚 Automates disponibles :", list_saved_automates())
    try:
        name = input("Nom de l'automate à charger : ")
        automate = load_automate(name)
        print(f"📖 Contenu de l'automate : {automate}")
    except FileNotFoundError as e:
        print(e)
