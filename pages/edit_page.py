import streamlit as st
from models.etat import Etat
from models.transition import Transition
from utils.json_handler import delete_automate
from visualizations.graph_viewer import visualize_automate

def edit_automate_page():
    st.header("✏️ Modifier l'automate")
    
    if 'current_automate' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord charger un automate.")
        return
    
    automate = st.session_state['current_automate']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Modifications")
        
        # Modification des états
        with st.expander("États"):
            # Ajout d'état
            new_state = st.text_input("Nouvel état", key="new_state")
            is_initial = st.checkbox("État initial")
            is_final = st.checkbox("État final")
            if st.button("Ajouter l'état"):
                if new_state:
                    if new_state not in [e.nom for e in automate.etats]:
                        automate.etats.append(Etat(new_state, is_initial, is_final))
                        st.success(f"✅ État '{new_state}' ajouté")
                    else:
                        st.error("❌ Cet état existe déjà")
            
            # Suppression d'état
            state_to_delete = st.selectbox(
                "État à supprimer",
                [e.nom for e in automate.etats]
            )
            if st.button("Supprimer l'état"):
                automate.etats = [e for e in automate.etats if e.nom != state_to_delete]
                automate.transitions = [t for t in automate.transitions 
                                     if t.etat_depart != state_to_delete 
                                     and t.etat_arrive != state_to_delete]
                st.success(f"✅ État '{state_to_delete}' supprimé")
        
        # Modification de l'alphabet
        with st.expander("Alphabet"):
            new_symbol = st.text_input("Nouveau symbole")
            if st.button("Ajouter le symbole"):
                if new_symbol and new_symbol not in automate.alphabet.symboles:
                    automate.alphabet.symboles.append(new_symbol)
                    st.success(f"✅ Symbole '{new_symbol}' ajouté")
            
            symbol_to_delete = st.selectbox(
                "Symbole à supprimer",
                automate.alphabet.symboles
            )
            if st.button("Supprimer le symbole"):
                automate.alphabet.symboles.remove(symbol_to_delete)
                automate.transitions = [t for t in automate.transitions 
                                     if t.symbole != symbol_to_delete]
                st.success(f"✅ Symbole '{symbol_to_delete}' supprimé")
        
        # Modification des transitions
        with st.expander("Transitions"):
            # Ajout de transition
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                etat_depart = st.selectbox("État départ", [e.nom for e in automate.etats])
            with col_t2:
                symbole = st.selectbox("Symbole", automate.alphabet.symboles)
            with col_t3:
                etat_arrive = st.selectbox("État arrivée", [e.nom for e in automate.etats])
            
            if st.button("Ajouter la transition"):
                new_trans = Transition(etat_depart, symbole, etat_arrive)
                if new_trans not in automate.transitions:
                    automate.transitions.append(new_trans)
                    st.success("✅ Transition ajoutée")
            
            # Liste et suppression des transitions
            st.write("Transitions existantes:")
            for i, t in enumerate(automate.transitions):
                if st.checkbox(f"{t.etat_depart} --{t.symbole}--> {t.etat_arrive}", key=f"trans_{i}"):
                    automate.transitions.remove(t)
                    st.success("✅ Transition supprimée")
        
        # Suppression de l'automate
        if st.button("🗑️ Supprimer l'automate", type="secondary"):
            if delete_automate(automate.nom):
                del st.session_state['current_automate']
                st.success(f"✅ Automate '{automate.nom}' supprimé")
                st.rerun()
    
    with col2:
        st.subheader("📊 Visualisation")
        try:
            fig = visualize_automate(automate, return_fig=True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Erreur de visualisation: {str(e)}") 