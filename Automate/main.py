import sys
from gui.app import AutomateApp
from services.automate_manager import AutomateManager

def start_console_mode():
   
    while True:
        print("\n===== Gestion des Automates (Console) =====")
        print("1. Créer un nouvel automate")
        print("2. Charger et afficher un automate")
        print("3. Lister les automates existants")
        print("4. Quitter")

        choice = input("Choisissez une option : ").strip()

        if choice == '1':
            AutomateManager.create_automate_console()
        elif choice == '2':
            AutomateManager.load_and_display_automate()
        elif choice == '3':
            from utils.json_handler import list_saved_automates
            automates = list_saved_automates()
            if automates:
                print("📚 Automates disponibles :", ", ".join(automates))
            else:
                print("❌ Aucun automate sauvegardé.")
        elif choice == '4':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option invalide. Veuillez réessayer.")

def start_gui_mode():
    app = AutomateApp()
    app.mainloop()

if __name__ == "__main__":
    print("===== Application de Gestion des Automates =====")
    print("1. Lancer en Mode Console")
    print("2. Lancer en Mode Graphique (GUI)")
    print("3. Quitter")

    mode = input("Sélectionnez le mode : ").strip()

    if mode == '1':
        start_console_mode()
    elif mode == '2':
        start_gui_mode()
    else:
        print("👋 Fin de l'application.")
        sys.exit(0)
