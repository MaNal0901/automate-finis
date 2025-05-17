import tkinter as tk
from tkinter import ttk, messagebox
from gui.automate_form import AutomateForm
from utils.json_handler import load_automate, list_saved_automates
from visualizations.graph_viewer import visualize_automate
from services.analysis_tools import est_deterministe, completer_automate, est_complet, determiniser_afn, minimiser_automate
from services.simulation_tools import simulate_word as simulate
class AutomateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Automates Finis")
        self.geometry("800x600")
        self.current_automate = None

        self.create_menu()
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        menubar = tk.Menu(self)

        # Automates
        automate_menu = tk.Menu(menubar, tearoff=0)
        automate_menu.add_command(label="Créer un automate", command=self.show_create_form)
        automate_menu.add_command(label="Charger un automate", command=self.show_load_form)
        automate_menu.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Automates", menu=automate_menu)

        # Analyse
        analyse_menu = tk.Menu(menubar, tearoff=0)
        analyse_menu.add_command(label="Vérifier Déterminisme", command=self.check_determinism)
        analyse_menu.add_command(label="Compléter l'automate", command=self.complete_automate)
        analyse_menu.add_command(label="Minimiser l'automate", command=self.minimize_automate)
        menubar.add_cascade(label="Analyse", menu=analyse_menu)

        # Avancée (Simulation, etc.)
        avance_menu = tk.Menu(menubar, tearoff=0)
        avance_menu.add_command(label="Afficher le graphe", command=self.display_graph)
        avance_menu.add_command(label="Simuler un mot", command=self.simulate_word)
        menubar.add_cascade(label="Avancée", menu=avance_menu)

        self.config(menu=menubar)

    def show_create_form(self):
        self.clear_main_frame()
        form = AutomateForm(self.main_frame)
        form.pack(fill=tk.BOTH, expand=True)

    def show_load_form(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Sélectionnez un automate à charger :").pack(pady=10)
        automates = list_saved_automates()
        selected = tk.StringVar()

        combo = ttk.Combobox(self.main_frame, values=automates, textvariable=selected)
        combo.pack(pady=10)

        def load_selected():
            try:
                self.current_automate = load_automate(selected.get())
                messagebox.showinfo("Succès", f"Automate '{selected.get()}' chargé.")
            except FileNotFoundError:
                messagebox.showerror("Erreur", "Automate non trouvé.")

        tk.Button(self.main_frame, text="Charger", command=load_selected).pack(pady=5)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def check_determinism(self):
        if self.current_automate:
            result = est_deterministe(self.current_automate)
            msg = "✅ L'automate est déterministe." if result else "❌ L'automate est non déterministe."
            messagebox.showinfo("Déterminisme", msg)
        else:
            messagebox.showwarning("Attention", "Aucun automate chargé.")

    def complete_automate(self):
        if self.current_automate:
            if est_complet(self.current_automate):
                messagebox.showinfo("Complétion", "✅ L'automate est déjà complet.")
            else:
                self.current_automate = completer_automate(self.current_automate)
                messagebox.showinfo("Complétion", "✅ Automate complété avec succès.")
        else:
            messagebox.showwarning("Attention", "Aucun automate chargé.")

    def minimize_automate(self):
        if self.current_automate:
            from utils.json_handler import save_automate
            minimized = minimiser_automate(self.current_automate)
            save_automate(minimized, minimized.nom)
            messagebox.showinfo("Minimisation", f"✅ Automate minimisé et sauvegardé sous '{minimized.nom}'.")
        else:
            messagebox.showwarning("Attention", "Aucun automate chargé.")

    def display_graph(self):
        if self.current_automate:
            visualize_automate(self.current_automate)
        else:
            messagebox.showwarning("Attention", "Aucun automate chargé.")

    def simulate_word(self):
        if not self.current_automate:
            messagebox.showwarning("Attention", "Aucun automate chargé.")
            return
        word = tk.simpledialog.askstring("Simulation", "Entrez un mot à tester :")
        
        accepted = simulate(self.current_automate, word)
        msg = f"✅ Le mot '{word}' est accepté." if accepted else f"❌ Le mot '{word}' est rejeté."
        messagebox.showinfo("Résultat de la Simulation", msg)

if __name__ == "__main__":
    app = AutomateApp()
    app.mainloop()