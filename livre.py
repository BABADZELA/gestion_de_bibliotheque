from dataclasses import dataclass

from db import conn

@dataclass
class Livre:
    """_summary_
    """
    titre: str 
    auteur: str  
    isbn: str
    type_livre: str 
    disponible: int = 1

    def __str__(self) -> str:
        return f"Livre: {self.titre}, écrit par: {self.auteur}, (ISBN: {self.isbn}, Type de livre: {self.type_livre})"


    def mis_a_jour(self, isbn):
        # avant de mettre à jour les information d'un livre, on vérifie qu'il existe bien dans la base
        with conn:
            cur = conn.cursor()
            livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [isbn]).fetchone()

            if not livre:
                print("Le livre spécifié n'existe pas et on renvoie le formulaire pour changer isbn")
            else:
                # si la requête retourne un résultat nous mettons à jour les résultats
                cur.execute('UPDATE Livre SET titre = ?, auteur = ?, type = ? WHERE isbn = ?', (self.titre, self.auteur, self.type_livre, isbn))
                print("Mis à jour reussi")
            

    def supprimer(self) -> str:
        # avant de supprimer un livre de la base on vérifie que l'utilisateur a bien le droit de 
        # le faire et que le livre existe bel et bien dans la base
        with conn:
            cur = conn.cursor()
            # livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [self.isbn]).fetchone()
            cur.execute('DELETE FROM Livre WHERE isbn = ?', (self.isbn,))
            # conn.commit()
            return "Le livre a bien été supprimé"


if __name__ == '__main__':
    livre = Livre("Moby Dick", "Herman Melville", "978-0-57-148410-7", "Papier")

