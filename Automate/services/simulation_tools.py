from models.automate import Automate

def simulate_word(automate: Automate, word: str) -> bool:
    """Simule l'exécution d'un mot sur l'automate et retourne s'il est accepté ou rejeté."""
    
    # Recherche des états initiaux
    current_states = [e.nom for e in automate.etats if e.est_initial]

    for symbole in word:
        next_states = set()
        for etat in current_states:
            for t in automate.transitions:
                if t.etat_depart == etat and t.symbole == symbole:
                    next_states.add(t.etat_arrive)
        current_states = list(next_states)
        if not current_states:
            return False  # Aucun état atteint, mot rejeté directement

    # Vérification des états finaux
    final_states = [e.nom for e in automate.etats if e.est_final]
    return any(state in final_states for state in current_states)

# Test rapide
if __name__ == "__main__":
    from utils.json_handler import load_automate

    try:
        automate_name = input("Nom de l'automate à charger : ")
        automate = load_automate(automate_name)
        word = input("Entrez le mot à tester : ")
        accepted = simulate_word(automate, word)
        print(f"Résultat : {'✅ Accepté' if accepted else '❌ Rejeté'}")
    except FileNotFoundError:
        print("❌ Automate non trouvé.")
