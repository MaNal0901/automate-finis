class Alphabet:
    def __init__(self, symboles):
        self.symboles = set(symboles)

    def to_dict(self):
        return {"symboles": list(self.symboles)}

    @staticmethod
    def from_dict(data):
        return Alphabet(data["symboles"])

    def __repr__(self):
        return f"Alphabet({self.symboles})"
