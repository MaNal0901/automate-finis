class Etat:
    def __init__(self, nom, est_initial=False, est_final=False):
        self.nom = nom
        self.est_initial = est_initial
        self.est_final = est_final

    def to_dict(self):
        return {
            "nom": self.nom,
            "est_initial": self.est_initial,
            "est_final": self.est_final
        }

    @staticmethod
    def from_dict(data):
        return Etat(
            data["nom"],
            data["est_initial"],
            data["est_final"]
        )

    def __repr__(self):
        return f"Etat({self.nom}, initial={self.est_initial}, final={self.est_final})" 