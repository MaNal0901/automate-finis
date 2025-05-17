class Transition:
    def __init__(self, etat_depart, symbole, etat_arrive):
        self.etat_depart = etat_depart
        self.symbole = symbole
        self.etat_arrive = etat_arrive

    def to_dict(self):
        return {
            "etat_depart": self.etat_depart,
            "symbole": self.symbole,
            "etat_arrive": self.etat_arrive
        }

    @staticmethod
    def from_dict(data):
        return Transition(data["etat_depart"], data["symbole"], data["etat_arrive"])

    def __repr__(self):
        return f"Transition({self.etat_depart} --{self.symbole}--> {self.etat_arrive})"
