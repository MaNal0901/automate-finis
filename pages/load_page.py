import streamlit as st
from utils.json_handler import load_automate, list_saved_automates
from visualizations.graph_viewer import visualize_automate

def load_automate_page():
    st.header("📂 Charger un automate")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        automates = list_saved_automates()
        if not automates:
            st.warning("⚠️ Aucun automate sauvegardé.")
            return
        
        selected = st.selectbox(
            "🔍 Sélectionnez un automate",
            automates,
            help="Choisissez un automate dans la liste"
        )
        
        if st.button("📥 Charger l'automate", key="load_button"):
            try:
                automate = load_automate(selected)
                st.session_state['current_automate'] = automate
                st.success(f"✅ Automate '{selected}' chargé avec succès!")
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement: {str(e)}")
    
    with col2:
        if 'current_automate' in st.session_state:
            automate = st.session_state['current_automate']
            
            st.subheader("ℹ️ Informations")
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown(f"""
                **🔵 États:** {', '.join(e.nom for e in automate.etats)}  
                **🔤 Alphabet:** {', '.join(automate.alphabet.symboles)}
                
                **🎨 Légende des états:**
                - 🟠 État initial et final
                - 🟡 État initial 
                - 🟢 État final 
                - 🔵 État normal 
                """)
            
            with info_col2:
                st.markdown(f"""
                **➡️ État initial:** {next(e.nom for e in automate.etats if e.est_initial)}  
                **🎯 États finaux:** {', '.join(e.nom for e in automate.etats if e.est_final)}
                """)
            
            st.subheader("📊 Visualisation")
            try:
                fig = visualize_automate(automate, return_fig=True)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"❌ Erreur de visualisation: {str(e)}") 