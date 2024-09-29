class User:
    def __init__(self, nom: str, type_utilisateur: str):
        self.nom = nom
        self.type_utilisateur = type_utilisateur.lower()

    def __str__(self):
        return f"{self.nom}:{self.type_utilisateur}"
    