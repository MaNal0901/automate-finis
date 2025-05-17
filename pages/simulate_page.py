import streamlit as st
from services.simulation_tools import simulate_word
from services.analysis_tools import generer_mots_acceptes, generer_mots_rejetes
from visualizations.graph_viewer import visualize_automate

def simulate_automate_page():
    st.header("▶️ Simuler l'automate")
    
    if 'current_automate' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord charger un automate.")
        return
    
    automate = st.session_state['current_automate']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎮 Test de mots")
        word = st.text_input(
            "📝 Entrez un mot à tester",
            placeholder=f"Utilisez les symboles : {', '.join(automate.alphabet.symboles)}"
        )
        
        if st.button("▶️ Tester le mot"):
            if not word:
                st.warning("⚠️ Veuillez entrer un mot à tester")
                return
            
            # Vérification des symboles
            invalid_symbols = [s for s in word if s not in automate.alphabet.symboles]
            if invalid_symbols:
                st.error(f"❌ Symboles invalides : {', '.join(invalid_symbols)}")
                return
            
            try:
                result = simulate_word(automate, word)
                if result:
                    st.success(f"✅ Le mot '{word}' est accepté")
                else:
                    st.error(f"❌ Le mot '{word}' est rejeté")
            except Exception as e:
                st.error(f"❌ Erreur lors de la simulation: {str(e)}")
        
        st.subheader("📝 Génération de mots")
        longueur_max = st.number_input(
            "Longueur maximale",
            min_value=0,
            max_value=10,
            value=3
        )
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            if st.button("✨ Mots acceptés"):
                try:
                    mots = generer_mots_acceptes(automate, longueur_max)
                    if mots:
                        st.success(f"Mots acceptés (longueur ≤ {longueur_max}):")
                        st.write(", ".join(mots) if mots else "Aucun mot")
                    else:
                        st.info("Aucun mot accepté trouvé")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
        
        with col_g2:
            if st.button("✨ Mots rejetés"):
                try:
                    mots = generer_mots_rejetes(automate, longueur_max)
                    if mots:
                        st.success(f"Mots rejetés (longueur ≤ {longueur_max}):")
                        st.write(", ".join(mots) if mots else "Aucun mot")
                    else:
                        st.info("Aucun mot rejeté trouvé")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
    
    with col2:
        st.subheader("📊 Visualisation")
        try:
            fig = visualize_automate(automate, return_fig=True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Erreur de visualisation: {str(e)}") 