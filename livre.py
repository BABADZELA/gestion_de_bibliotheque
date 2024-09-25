from dataclasses import dataclass

from db import conn, cur
from user import User


@dataclass
class Livre:
    """_summary_
    """
    titre: str 
    auteur: str  
    isbn: str
    type_livre: str 

    def ajouter(self, titre: str, auteur: str, isbn: str, type_livre: str) -> None:
        cur.execute("INSERT INTO Livre VALUES(?, ?, ?, ?)", (titre, auteur, isbn, type_livre))
        conn.commit()
        conn.close()

    def mis_a_jour(self, isbn):
        # avant de mettre à jour les information d'un livre, on vérifie s'il existe bien dans la base
        livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [isbn]).fetchone()

        if not livre:
            print("Le livre spécifié n'existe pas et on renvoie le formulaire pour changer isbn")
        else:
            # cur = conn.cursor()
            # si la requête retourne un résultat nous mettons à jour les résultats
            cur.execute('UPDATE Livre SET titre = ?, auteur = ?, type = ? WHERE isbn = ?', (self.titre, self.auteur, self.type_livre, isbn))
            print("Mis à jour reussi")
        
        conn.commit()
        conn.close()
            

    def supprimer(self, isbn):
        # avant de supprimer un livre de la base on vérifie que l'utilisateur a bien le droit de 
        # le faire et que le livre existe bel et bien dans la base
        livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [isbn]).fetchone()

        if not livre:
            print(f"ISBN: {isbn} n'existe pas ")
        else:
            cur.execute('DELETE FROM Livre WHERE isbn = ?', (isbn,))
            conn.commit()
            print("Le livre a bien été supprimé")

        conn.close()


    def rechercher(self, param: str, value: str) -> None:
        """Cette fonction permet de rechercher un livre dans la base en utilisant soit:
        - isbn
        - titre
        - auteur

        Args:
            param (str): Ce paramètre va contenir le choix de l'utilisateur parmi les 3 ci-dessus
            value (str): Correspond à la valeur du choix
        """
        # vu que l'utilisateur peut faire sa recherche sur 3 critères: titre, auteur ou isbn
        # je gère ci-dessous les trois cas
        if param.lower() == 'isbn':
            cur.execute("SELECT * FROM Livre WHERE isbn like ?", (value,))
        elif param.lower() == 'titre':
            for row in cur.execute("SELECT * FROM Livre WHERE titre like ?", (value,)):
                print(row)
        elif param.lower() == 'auteur':
            for row in cur.execute("SELECT * FROM Livre WHERE auteur like ?", (value,)):
                print(row)
        conn.commit()
        conn.close()

    def emprunter(self, isbn, emprunteur):
        # Avant de pouvoir emprunter un livre on doit vérifier qu'il est bien disponible
        livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn and disponible LIKE True", [isbn]).fetchone()

        if not livre:
            print("Le livre n'est pas disponible")
        else:
            cur.execute("INSERT INTO Emprunt VALUES(?, ?)", (isbn, emprunteur))
            # On met la valeur de disponible à faux vu celui-ci a été emprunté
            cur.execute('UPDATE Livre SET disponible = False WHERE isbn = ?', (isbn,))
        conn.commit()
        conn.close()

    def retourner(self, isbn):
        cur.execute('UPDATE Livre SET disponible = False WHERE isbn = ?', (isbn,))
        conn.commit()
        conn.close()

    def lister():
        for row in cur.execute("SELECT * FROM Livre"):
            print(row)

    def statistiques(self):
        pass
"""     o	Nombre total de livres
o	Nombre de livres empruntés
o	Nombre total d'utilisateurs
o	Livres les plus empruntés """



if __name__ == '__main__':
    livre = Livre("Quichotte","Miguel de Cervantes","978-3322114455", "papier")
    # livre.supprimer('978-3322114455')
    if livre:
        print("Super")
