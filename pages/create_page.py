import streamlit as st
from models.etat import Etat
from models.alphabet import Alphabet
from models.transition import Transition
from models.automate import Automate
from utils.json_handler import save_automate
from visualizations.graph_viewer import visualize_automate

def create_automate_page():
    st.header("📝 Créer un nouvel automate")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("create_automate"):
            nom = st.text_input("🏷️ Nom de l'automate")
            etats = st.text_input("🔵 États (séparés par des espaces)", placeholder="Ex: q0 q1 q2")
            alphabet = st.text_input("🔤 Alphabet (séparés par des espaces)", placeholder="Ex: a b")
            etat_initial = st.text_input("➡️ État initial", placeholder="Ex: q0")
            etats_finaux = st.text_input("🎯 États finaux (séparés par des espaces)", placeholder="Ex: q1 q2")
            transitions = st.text_area(
                "↔️ Transitions",
                placeholder="Format: etat_depart symbole etat_arrive\nEx:\nq0 a q1\nq1 b q2",
                height=150
            )
            
            submitted = st.form_submit_button("✨ Créer l'automate")
            
            if submitted:
                if not all([nom, etats, alphabet, etat_initial, etats_finaux, transitions]):
                    st.error("❌ Tous les champs sont obligatoires")
                    return
                
                try:
                    etats_list = etats.split()
                    alphabet_list = alphabet.split()
                    etats_finaux_list = etats_finaux.split()
                    
                    if etat_initial not in etats_list:
                        st.error("❌ L'état initial doit faire partie des états définis")
                        return
                    
                    for ef in etats_finaux_list:
                        if ef not in etats_list:
                            st.error(f"❌ L'état final {ef} n'est pas dans la liste des états")
                            return
                    
                    # Création des états
                    etats_obj = [Etat(n, n == etat_initial, n in etats_finaux_list) for n in etats_list]
                    
                    # Création de l'alphabet
                    alphabet_obj = Alphabet(alphabet_list)
                    
                    # Création des transitions
                    transitions_obj = []
                    for line in transitions.strip().split('\n'):
                        if line.strip():
                            try:
                                depart, symbole, arrive = line.strip().split()
                                if depart not in etats_list:
                                    st.error(f"❌ État de départ invalide : {depart}")
                                    return
                                if arrive not in etats_list:
                                    st.error(f"❌ État d'arrivée invalide : {arrive}")
                                    return
                                if symbole not in alphabet_list:
                                    st.error(f"❌ Symbole invalide : {symbole}")
                                    return
                                transitions_obj.append(Transition(depart, symbole, arrive))
                            except ValueError:
                                st.error(f"❌ Format de transition invalide : {line}")
                                return
                    
                    # Création de l'automate
                    automate = Automate(nom, etats_obj, alphabet_obj, transitions_obj)
                    save_automate(automate, nom)
                    st.session_state['current_automate'] = automate
                    st.success(f"✅ Automate '{nom}' créé avec succès!")
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de la création de l'automate: {str(e)}")
    
    with col2:
        st.info("""
        ℹ️ **Instructions:**
        
        1. **Nom**: Donnez un nom unique à votre automate
        2. **États**: Liste d'états séparés par des espaces (ex: q0 q1 q2)
        3. **Alphabet**: Symboles séparés par des espaces (ex: a b)
        4. **État initial**: Un seul état parmi les états listés
        5. **États finaux**: Un ou plusieurs états parmi les états listés
        6. **Transitions**: Une transition par ligne au format:
           `état_départ symbole état_arrivée`
        """)
        
        if 'current_automate' in st.session_state:
            st.subheader("📊 Visualisation")
            try:
                fig = visualize_automate(st.session_state['current_automate'], return_fig=True)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"❌ Erreur de visualisation: {str(e)}") 