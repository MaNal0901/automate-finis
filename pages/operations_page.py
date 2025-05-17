import streamlit as st
from services.analysis_tools import (
    sont_equivalents, union_automates, intersection_automates,
    complement_automate, determiniser_afn
)
from utils.json_handler import load_automate, list_saved_automates, save_automate
from visualizations.graph_viewer import visualize_automate

def operations_automate_page():
    st.header("🔄 Opérations sur les automates")
    
    if 'current_automate' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord charger un automate.")
        return
    
    automate = st.session_state['current_automate']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔀 Opérations binaires")
        
        # Sélection du second automate
        autres_automates = [a for a in list_saved_automates() if a != automate.nom]
        if not autres_automates:
            st.warning("⚠️ Pas d'autres automates disponibles pour les opérations")
            return
        
        automate2_nom = st.selectbox(
            "Sélectionnez le second automate",
            autres_automates
        )
        automate2 = load_automate(automate2_nom)
        fig = visualize_automate(automate2, return_fig=True)
        st.pyplot(fig)
        longueur_max = st.number_input("Longueur maximale des mots à tester", min_value=1, value=5)
        try:
            
            # Test d'équivalence
            if st.button("🔍 Tester l'équivalence"):
                if sont_equivalents(automate, automate2, longueur_max):
                    st.success("✅ Les automates sont équivalents")
                else:
                    st.error("❌ Les automates ne sont pas équivalents")
            
            # Union
            if st.button("🔄 Calculer l'union"):
                try:
                    union = union_automates(automate, automate2)
                    save_automate(union, union.nom)
                    st.session_state['current_automate'] = union
                    st.success("✅ Union calculée avec succès")
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors du calcul de l'union: {str(e)}")
            
            # Intersection
            if st.button("🔄 Calculer l'intersection"):
                try:
                    inter = intersection_automates(automate, automate2)
                    save_automate(inter, inter.nom)
                    st.session_state['current_automate'] = inter
                    st.success("✅ Intersection calculée avec succès")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors du calcul de l'intersection: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du second automate: {str(e)}")
        
        st.subheader("🔄 Opérations unaires")
        
        # Complément
        if st.button("🔄 Calculer le complément"):
            try:
                comp = complement_automate(automate)
                save_automate(comp, comp.nom)
                st.session_state['current_automate'] = comp
                st.success("✅ Complément calculé avec succès")
                
            except Exception as e:
                st.error(f"❌ Erreur lors du calcul du complément: {str(e)}")
        
        # Déterminisation
        if st.button("🔄 Déterminiser"):
            try:
                det = determiniser_afn(automate)
                save_automate(det, det.nom)
                st.session_state['current_automate'] = det
                st.success("✅ Automate déterminisé avec succès")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Erreur lors de la déterminisation: {str(e)}")
    
    with col2:
        st.subheader("📊 Visualisation")
        try:
            fig = visualize_automate(automate, return_fig=True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Erreur de visualisation: {str(e)}")