from models.automate import Automate
from models.etat import Etat
from models.transition import Transition
from itertools import product
from services.simulation_tools import simulate_word


def est_deterministe(automate: Automate) -> bool:
    """Vérifie si l'automate est déterministe."""
    # Un seul état initial
    etats_initiaux = [e for e in automate.etats if e.est_initial]
    if len(etats_initiaux) != 1:
        return False
    
    # Pour chaque état et symbole, au plus une transition
    for etat in automate.etats:
        for symbole in automate.alphabet.symboles:
            transitions = [t for t in automate.transitions 
                         if t.etat_depart == etat.nom and t.symbole == symbole]
            if len(transitions) > 1:
                return False
    
    return True

def est_complet(automate: Automate) -> bool:
    """Vérifie si l'automate est complet."""
    for etat in automate.etats:
        for symbole in automate.alphabet.symboles:
            transitions = [t for t in automate.transitions 
                         if t.etat_depart == etat.nom and t.symbole == symbole]
            if not transitions:
                return False
    return True

def completer_automate(automate: Automate) -> Automate:
    """Complète l'automate en ajoutant un état puits si nécessaire."""
    if est_complet(automate):
        return automate
    
    # Création d'une copie de l'automate
    new_etats = [Etat(e.nom, e.est_initial, e.est_final) for e in automate.etats]
    new_transitions = [Transition(t.etat_depart, t.symbole, t.etat_arrive) 
                      for t in automate.transitions]
    
    # Ajout de l'état puits
    puits = Etat("puits")
    new_etats.append(puits)
    
    # Ajout des transitions manquantes vers l'état puits
    for etat in automate.etats:
        for symbole in automate.alphabet.symboles:
            transitions = [t for t in automate.transitions 
                         if t.etat_depart == etat.nom and t.symbole == symbole]
            if not transitions:
                new_transitions.append(Transition(etat.nom, symbole, "puits"))
    
    # Ajout des transitions de l'état puits vers lui-même
    for symbole in automate.alphabet.symboles:
        new_transitions.append(Transition("puits", symbole, "puits"))
    
    return Automate(f"{automate.nom}_complet", new_etats, automate.alphabet, new_transitions)

def minimiser_automate(automate: Automate) -> Automate:
    """Minimise l'automate (version simplifiée)."""
    # Pour cet exemple, on retourne simplement une copie de l'automate
    # Une vraie implémentation nécessiterait l'algorithme de minimisation
    new_etats = [Etat(e.nom, e.est_initial, e.est_final) for e in automate.etats]
    new_transitions = [Transition(t.etat_depart, t.symbole, t.etat_arrive) 
                      for t in automate.transitions]
    return Automate(f"{automate.nom}_minimal", new_etats, automate.alphabet, new_transitions)

def determiniser_afn(automate: Automate) -> Automate:
    """Déterminise un automate fini non-déterministe."""
    if est_deterministe(automate):
        return automate

    # Initialisation
    etats_initiaux = frozenset(e.nom for e in automate.etats if e.est_initial)
    nouveaux_etats = {etats_initiaux}
    etats_a_traiter = [etats_initiaux]
    transitions_det = []
    etats_det = []
    etats_finaux_det = set()

    # Création des nouveaux états et transitions
    while etats_a_traiter:
        etat_courant = etats_a_traiter.pop(0)
        nom_etat = '_'.join(sorted(etat_courant)) or 'vide'

        # Pour chaque symbole de l'alphabet
        for symbole in automate.alphabet.symboles:
            etats_cibles = set()
            for etat in etat_courant:
                for t in automate.transitions:
                    if t.etat_depart == etat and t.symbole == symbole:
                        etats_cibles.add(t.etat_arrive)
            
            if etats_cibles:
                etats_cibles = frozenset(etats_cibles)
                nom_cible = '_'.join(sorted(etats_cibles))
                transitions_det.append(Transition(nom_etat, symbole, nom_cible))
                
                if etats_cibles not in nouveaux_etats:
                    nouveaux_etats.add(etats_cibles)
                    etats_a_traiter.append(etats_cibles)

        # Création de l'état
        est_initial = etat_courant == etats_initiaux
        est_final = any(e.nom in etat_courant for e in automate.etats if e.est_final)
        etats_det.append(Etat(nom_etat, est_initial, est_final))

    return Automate(f"{automate.nom}_deterministe", etats_det, automate.alphabet, transitions_det)

def generer_mots_acceptes(automate: Automate, longueur_max: int) -> list:
    """Génère tous les mots acceptés jusqu'à une longueur donnée."""
    mots_acceptes = []
    
    # Génération de tous les mots possibles jusqu'à longueur_max
    for longueur in range(longueur_max + 1):
        for mot in product(automate.alphabet.symboles, repeat=longueur):
            mot = ''.join(mot)
            if simulate_word(automate, mot):
                mots_acceptes.append(mot)
    
    return sorted(mots_acceptes)

def generer_mots_rejetes(automate: Automate, longueur_max: int) -> list:
    """Génère tous les mots rejetés jusqu'à une longueur donnée."""
    mots_rejetes = []
    
    # Génération de tous les mots possibles jusqu'à longueur_max
    for longueur in range(longueur_max + 1):
        for mot in product(automate.alphabet.symboles, repeat=longueur):
            mot = ''.join(mot)
            if not simulate_word(automate, mot):
                mots_rejetes.append(mot)
    
    return sorted(mots_rejetes)

def sont_equivalents(automate1: Automate, automate2: Automate, longueur_max: int = 5) -> bool:
    """Teste si deux automates sont équivalents jusqu'à une longueur donnée."""
    # Vérifie si les alphabets sont identiques
    if set(automate1.alphabet.symboles) != set(automate2.alphabet.symboles):
        return False
    
    # Compare les mots acceptés jusqu'à longueur_max
    mots1 = set(generer_mots_acceptes(automate1, longueur_max))
    mots2 = set(generer_mots_acceptes(automate2, longueur_max))
    
    return mots1 == mots2

def union_automates(automate1: Automate, automate2: Automate) -> Automate:
    """Calcule l'union de deux automates."""
    # Vérification des alphabets
    if set(automate1.alphabet.symboles) != set(automate2.alphabet.symboles):
        raise ValueError("Les alphabets des automates doivent être identiques")
    
    # Préfixe pour éviter les conflits de noms
    prefix1, prefix2 = "A1_", "A2_"
    
    # Création des nouveaux états
    new_etats = []
    for e in automate1.etats:
        new_etats.append(Etat(prefix1 + e.nom, e.est_initial, e.est_final))
    for e in automate2.etats:
        new_etats.append(Etat(prefix2 + e.nom, e.est_initial, e.est_final))
    
    # Création des nouvelles transitions
    new_transitions = []
    for t in automate1.transitions:
        new_transitions.append(Transition(
            prefix1 + t.etat_depart,
            t.symbole,
            prefix1 + t.etat_arrive
        ))
    for t in automate2.transitions:
        new_transitions.append(Transition(
            prefix2 + t.etat_depart,
            t.symbole,
            prefix2 + t.etat_arrive
        ))
    
    return Automate(
        f"{automate1.nom}_union_{automate2.nom}",
        new_etats,
        automate1.alphabet,
        new_transitions
    )

def intersection_automates(automate1: Automate, automate2: Automate) -> Automate:
    """Calcule l'intersection de deux automates."""
    # Vérification des alphabets
    if set(automate1.alphabet.symboles) != set(automate2.alphabet.symboles):
        raise ValueError("Les alphabets des automates doivent être identiques")
    
    # Création des états du produit cartésien
    new_etats = []
    new_transitions = []
    
    # Pour chaque paire d'états
    for e1 in automate1.etats:
        for e2 in automate2.etats:
            nom = f"{e1.nom}_{e2.nom}"
            est_initial = e1.est_initial and e2.est_initial
            est_final = e1.est_final and e2.est_final
            new_etats.append(Etat(nom, est_initial, est_final))
    
    # Pour chaque symbole et paire d'états
    for e1 in automate1.etats:
        for e2 in automate2.etats:
            for symbole in automate1.alphabet.symboles:
                # Trouve les transitions correspondantes
                trans1 = [t for t in automate1.transitions 
                         if t.etat_depart == e1.nom and t.symbole == symbole]
                trans2 = [t for t in automate2.transitions 
                         if t.etat_depart == e2.nom and t.symbole == symbole]
                
                # Crée les nouvelles transitions
                for t1 in trans1:
                    for t2 in trans2:
                        new_transitions.append(Transition(
                            f"{e1.nom}_{e2.nom}",
                            symbole,
                            f"{t1.etat_arrive}_{t2.etat_arrive}"
                        ))
    
    return Automate(
        f"{automate1.nom}_inter_{automate2.nom}",
        new_etats,
        automate1.alphabet,
        new_transitions
    )

def complement_automate(automate: Automate) -> Automate:
    """Calcule le complément d'un automate."""
    # D'abord, on s'assure que l'automate est déterministe et complet
    if not est_deterministe(automate):
        automate = determiniser_afn(automate)
    if not est_complet(automate):
        automate = completer_automate(automate)
    
    # Création des nouveaux états en inversant les états finaux
    new_etats = [
        Etat(e.nom, e.est_initial, not e.est_final)
        for e in automate.etats
    ]
    
    return Automate(
        f"{automate.nom}_complement",
        new_etats,
        automate.alphabet,
        automate.transitions.copy()
    ) 