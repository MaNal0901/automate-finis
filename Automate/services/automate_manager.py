from models.etat import Etat
from models.alphabet import Alphabet
from models.transition import Transition
from models.automate import Automate
from utils.json_handler import save_automate, load_automate, list_saved_automates
import os

class AutomateManager:
    @staticmethod
    def create_automate_console():
        nom = input("Nom de l'automate : ").strip()

        # États
        etats_noms = input("Noms des états (séparés par des espaces) : ").split()
        etats = [Etat(n) for n in etats_noms]

        # État Initial
        etat_initial_nom = input("Nom de l'état initial : ").strip()
        for e in etats:
            if e.nom == etat_initial_nom:
                e.est_initial = True

        # États Finaux
        etats_finaux_noms = input("Noms des états finaux (séparés par des espaces) : ").split()
        for e in etats:
            if e.nom in etats_finaux_noms:
                e.est_final = True

        # Alphabet
        alphabet_symbols = input("Symboles de l'alphabet (séparés par des espaces) : ").split()
        alphabet = Alphabet(alphabet_symbols)

        # Transitions
        transitions = []
        print("Définir les transitions (format: etat_depart symbole etat_arrive). Tapez 'fin' pour terminer.")
        while True:
            trans = input("Transition : ").strip()
            if trans.lower() == 'fin':
                break
            try:
                depart, symbole, arrive = trans.split()
                if depart in etats_noms and arrive in etats_noms and symbole in alphabet_symbols:
                    transitions.append(Transition(depart, symbole, arrive))
                else:
                    print("Erreur : état ou symbole non défini.")
            except ValueError:
                print("Format incorrect. Réessayez.")

        automate = Automate(nom, etats, alphabet, transitions)
        save_automate(automate, nom)
        print(f"✅ Automate '{nom}' créé et sauvegardé avec succès.")

    @staticmethod
    def load_and_display_automate():
        automates = list_saved_automates()
        if not automates:
            print("❌ Aucun automate sauvegardé.")
            return
        print("📚 Automates disponibles :", automates)
        nom = input("Nom de l'automate à charger : ").strip()
        try:
            automate = load_automate(nom)
            print(f"📖 Contenu de l'automate : {automate.to_dict()}")
        except FileNotFoundError:
            print("❌ Automate non trouvé.")
