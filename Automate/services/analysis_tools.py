from models.automate import Automate

def est_deterministe(automate: Automate):
    """Vérifie si l'automate est déterministe (AFD)."""
    transitions_seen = {}
    for t in automate.transitions:
        key = (t.etat_depart, t.symbole)
        if key in transitions_seen:
            return False  # Deux transitions pour le même état et symbole
        transitions_seen[key] = t.etat_arrive
    return True

def est_complet(automate: Automate):
    """Vérifie si l'automate est complet."""
    etats = [e.nom for e in automate.etats]
    symboles = automate.alphabet.symboles
    transitions = {(t.etat_depart, t.symbole) for t in automate.transitions}

    for e in etats:
        for s in symboles:
            if (e, s) not in transitions:
                return False
    return True

def completer_automate(automate: Automate):
    """Complète l'automate en ajoutant un état 'Puits' si nécessaire."""
    if est_complet(automate):
        print("✅ Automate déjà complet.")
        return automate

    if "Puits" not in [e.nom for e in automate.etats]:
        from models.etat import Etat
        automate.etats.append(Etat("Puits"))

    for e in automate.etats:
        for s in automate.alphabet.symboles:
            if not any(t for t in automate.transitions if t.etat_depart == e.nom and t.symbole == s):
                from models.transition import Transition
                automate.transitions.append(Transition(e.nom, s, "Puits"))

    print("✅ Automate complété avec l'état 'Puits'.")
    return automate

# Autres outils comme minimisation, transformation AFN → AFD, etc., peuvent être ajoutés ici.

def determiniser_afn(afn: Automate) -> Automate:
    """Transforme un AFN en AFD en utilisant la méthode des ensembles d'états."""

    from models.etat import Etat
    from models.transition import Transition
    from models.alphabet import Alphabet

    etats_afn = {e.nom: e for e in afn.etats}
    symboles = afn.alphabet.symboles
    initial_states = [e.nom for e in afn.etats if e.est_initial]

    afd_states = []
    afd_transitions = []
    visited = []
    state_mapping = {}

    queue = [frozenset(initial_states)]
    while queue:
        current_set = queue.pop(0)
        state_name = "_".join(sorted(current_set))

        if state_name not in state_mapping:
            is_initial = any(etats_afn[s].est_initial for s in current_set)
            is_final = any(etats_afn[s].est_final for s in current_set)
            afd_states.append(Etat(state_name, is_initial, is_final))
            state_mapping[current_set] = state_name

        for symbol in symboles:
            next_states = set()
            for state in current_set:
                for t in afn.transitions:
                    if t.etat_depart == state and t.symbole == symbol:
                        next_states.add(t.etat_arrive)
            if next_states:
                next_state_name = "_".join(sorted(next_states))
                afd_transitions.append(Transition(state_name, symbol, next_state_name))
                if frozenset(next_states) not in visited:
                    visited.append(frozenset(next_states))
                    queue.append(frozenset(next_states))

    afd_alphabet = Alphabet(symboles)
    afd = Automate(f"{afn.nom}_AFD", afd_states, afd_alphabet, afd_transitions)
    return afd
def minimiser_automate(afd: Automate) -> Automate:
    """Minimise un AFD en utilisant l'algorithme de Moore."""

    from models.etat import Etat
    from models.transition import Transition
    from models.alphabet import Alphabet

    # Étape 1 : Initialisation des partitions
    finals = {e.nom for e in afd.etats if e.est_final}
    non_finals = {e.nom for e in afd.etats if not e.est_final}
    partitions = [finals, non_finals]

    changed = True
    while changed:
        changed = False
        new_partitions = []
        for group in partitions:
            # Regrouper selon les transitions pour chaque symbole
            subgroups = {}
            for state in group:
                signature = []
                for symbol in afd.alphabet.symboles:
                    dest = next((t.etat_arrive for t in afd.transitions if t.etat_depart == state and t.symbole == symbol), None)
                    for idx, p in enumerate(partitions):
                        if dest in p:
                            signature.append(idx)
                            break
                    else:
                        signature.append(-1)
                signature = tuple(signature)
                subgroups.setdefault(signature, set()).add(state)
            new_partitions.extend(subgroups.values())
            if len(subgroups) > 1:
                changed = True
        partitions = new_partitions

    # Étape 2 : Création de l'automate minimal
    state_mapping = {}
    for idx, group in enumerate(partitions):
        name = f"P{idx}"
        for state in group:
            state_mapping[state] = name

    min_states = []
    for idx, group in enumerate(partitions):
        name = f"P{idx}"
        is_initial = any(e.nom in group and e.est_initial for e in afd.etats)
        is_final = any(e.nom in group and e.est_final for e in afd.etats)
        min_states.append(Etat(name, is_initial, is_final))

    min_transitions = []
    for t in afd.transitions:
        from_state = state_mapping[t.etat_depart]
        to_state = state_mapping[t.etat_arrive]
        if not any(tr for tr in min_transitions if tr.etat_depart == from_state and tr.symbole == t.symbole):
            min_transitions.append(Transition(from_state, t.symbole, to_state))

    min_automate = Automate(f"{afd.nom}_Minimized", min_states, Alphabet(afd.alphabet.symboles), min_transitions)
    return min_automate

