from models.etat import Etat
from models.alphabet import Alphabet
from models.transition import Transition

class Automate:
    def __init__(self, nom, etats=None, alphabet=None, transitions=None):
        self.nom = nom
        self.etats = etats if etats else []
        self.alphabet = alphabet if alphabet else Alphabet([])
        self.transitions = transitions if transitions else []

    def to_dict(self):
        return {
            "nom": self.nom,
            "etats": [e.to_dict() for e in self.etats],
            "alphabet": self.alphabet.to_dict(),
            "transitions": [t.to_dict() for t in self.transitions]
        }

    @staticmethod
    def from_dict(data):
        etats = [Etat.from_dict(e) for e in data["etats"]]
        alphabet = Alphabet.from_dict(data["alphabet"])
        transitions = [Transition.from_dict(t) for t in data["transitions"]]
        return Automate(data["nom"], etats, alphabet, transitions)

    def __repr__(self):
        return f"Automate({self.nom})" 