import streamlit as st
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from markdown import MARK_DOWN
from pages.create_page import create_automate_page
from pages.load_page import load_automate_page
from pages.edit_page import edit_automate_page
from pages.analyze_page import analyze_automate_page
from pages.operations_page import operations_automate_page
from pages.simulate_page import simulate_automate_page

# Configuration de la page
st.set_page_config(
    page_title="Gestion des Automates Finis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé avec des couleurs plus douces
st.markdown(MARK_DOWN, unsafe_allow_html=True)

def main():
    st.title("🔄 Gestion des Automates Finis")
    
    # Menu horizontal avec des onglets
    tabs = st.tabs([
        "📝 Créer",
        "📂 Charger",
        "✏️ Modifier",
        "🔍 Analyser",
        "🔄 Opérations",
        "▶️ Simuler"
    ])
    
    with tabs[0]:
        create_automate_page()
    with tabs[1]:
        load_automate_page()
    with tabs[2]:
        edit_automate_page()
    with tabs[3]:
        analyze_automate_page()
    with tabs[4]:
        operations_automate_page()
    with tabs[5]:
        simulate_automate_page()

if __name__ == "__main__":
    main() 