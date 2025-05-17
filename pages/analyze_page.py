import streamlit as st
from services.analysis_tools import est_deterministe, est_complet, completer_automate, minimiser_automate
from utils.json_handler import save_automate
from visualizations.graph_viewer import visualize_automate

def analyze_automate_page():
    st.header("🔍 Analyser l'automate")
    
    if 'current_automate' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord charger un automate.")
        return
    
    automate = st.session_state['current_automate']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔎 Propriétés")
        
        if st.button("🔄 Vérifier le déterminisme"):
            result = est_deterministe(automate)
            if result:
                st.success("✅ L'automate est déterministe")
            else:
                st.warning("⚠️ L'automate n'est pas déterministe")
        
        if st.button("🔄 Vérifier si complet"):
            result = est_complet(automate)
            if result:
                st.success("✅ L'automate est complet")
            else:
                st.warning("⚠️ L'automate n'est pas complet")
        
        st.subheader("🛠️ Transformations")
        
        if st.button("✨ Compléter l'automate"):
            if est_complet(automate):
                st.info("ℹ️ L'automate est déjà complet")
            else:
                try:
                    completed = completer_automate(automate)
                    save_automate(completed, f"{automate.nom}_complet")
                    st.session_state['current_automate'] = completed
                    st.success(f"✅ Automate complété et sauvegardé")
                except Exception as e:
                    st.error(f"❌ Erreur lors de la complétion: {str(e)}")
        
        if st.button("✨ Minimiser l'automate"):
            try:
                minimized = minimiser_automate(automate)
                save_automate(minimized, f"{automate.nom}_minimal")
                st.session_state['current_automate'] = minimized
                st.success(f"✅ Automate minimisé et sauvegardé")
            except Exception as e:
                st.error(f"❌ Erreur lors de la minimisation: {str(e)}")
    
    with col2:
        st.subheader("📊 Visualisation")
        try:
            fig = visualize_automate(automate, return_fig=True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Erreur de visualisation: {str(e)}") 