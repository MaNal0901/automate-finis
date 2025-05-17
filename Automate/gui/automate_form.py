import tkinter as tk
from tkinter import messagebox
from models.etat import Etat
from models.alphabet import Alphabet
from models.transition import Transition
from models.automate import Automate
from utils.json_handler import save_automate

class AutomateForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.nom_var = tk.StringVar()
        self.etats_var = tk.StringVar()
        self.alphabet_var = tk.StringVar()
        self.transitions_var = tk.StringVar()
        self.etat_initial_var = tk.StringVar()
        self.etats_finaux_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Nom de l'automate:").pack()
        tk.Entry(self, textvariable=self.nom_var).pack()

        tk.Label(self, text="États (séparés par des espaces):").pack()
        tk.Entry(self, textvariable=self.etats_var).pack()

        tk.Label(self, text="Alphabet (séparés par des espaces):").pack()
        tk.Entry(self, textvariable=self.alphabet_var).pack()

        tk.Label(self, text="Transitions (format: etat_depart symbole etat_arrive ; séparées par ;):").pack()
        tk.Entry(self, textvariable=self.transitions_var).pack()

        tk.Label(self, text="État Initial:").pack()
        tk.Entry(self, textvariable=self.etat_initial_var).pack()

        tk.Label(self, text="États Finaux (séparés par des espaces):").pack()
        tk.Entry(self, textvariable=self.etats_finaux_var).pack()

        tk.Button(self, text="Sauvegarder", command=self.save).pack(pady=10)

    def save(self):
        nom = self.nom_var.get()
        etats_noms = self.etats_var.get().split()
        alphabet_symbols = self.alphabet_var.get().split()
        transitions_input = self.transitions_var.get().split(';')
        etat_initial = self.etat_initial_var.get()
        etats_finaux = self.etats_finaux_var.get().split()

        # Création des objets
        etats = [Etat(n, n == etat_initial, n in etats_finaux) for n in etats_noms]
        alphabet = Alphabet(alphabet_symbols)
        transitions = []

        for t in transitions_input:
            parts = t.strip().split()
            if len(parts) == 3:
                depart, symbole, arrive = parts
                if depart in etats_noms and arrive in etats_noms and symbole in alphabet_symbols:
                    transitions.append(Transition(depart, symbole, arrive))
                else:
                    messagebox.showerror("Erreur", f"Transition invalide : {t}")
                    return
            else:
                messagebox.showerror("Erreur", "transition Syntax invalide")

        automate = Automate(nom, etats, alphabet, transitions)
        save_automate(automate, nom)
        messagebox.showinfo("Succès", f"Automate '{nom}' sauvegardé avec succès.")

