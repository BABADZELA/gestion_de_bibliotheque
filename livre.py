from dataclasses import dataclass

from db import conn
from user import User

def lister() -> None:
        with conn:
            cur = conn.cursor()
            for row in cur.execute("SELECT * FROM Livre"):
                print(f" - Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})")
        

def statistiques():
    with conn:
        cur = conn.cursor()
        # Nombre de livre dans la base
        nombre_de_livre = cur.execute('SELECT COUNT(*) FROM Livre').fetchone()
        # Nombre de livre emprunté
        nombre_de_livre_emprunté = cur.execute('SELECT COUNT(*) FROM Livre WHERE disponible is False').fetchone()
        # nombre total d'utilisateur
        nombre_d_utilisateur = cur.execute('SELECT COUNT(*) FROM User').fetchone()
        # Livres le plus emprunté
        # D'abord on vérifie que la table Emprunt n'est pas vide
        livre_emprunte = cur.execute('SELECT isbn FROM Emprunt').fetchone()

        if not livre_emprunte:
            livre_emprunte = "Pas de livres empruntés"
        else:
            livre_emprunte = cur.execute('SELECT isbn FROM Emprunt WHERE nombre = MAX(nombre)').fetchone()

        resultat = f"""

        =============== QUELQUES STATISTIQUES =============================

            - Nombre de livre: {nombre_de_livre[0]}
            - Nombre total d'utilisateur: {nombre_d_utilisateur[0]}
            - Nombre de livre emprunté: {nombre_de_livre_emprunté[0]}
            - L'ISBN du livre le plus emprunté: {livre_emprunte}

        ==================================================================
"""
        
        
        print(resultat)
    conn.close()

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

    def ajouter(self) -> None:
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Livre VALUES(?, ?, ?, ?, ?)", (self.titre, self.auteur, self.isbn, self.type_livre.lower(), self.disponible))
            # conn.commit()
            # conn.close()

    def mis_a_jour(self, isbn):
        # avant de mettre à jour les information d'un livre, on vérifie s'il existe bien dans la base
        with conn:
            cur = conn.cursor()
            livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [isbn]).fetchone()

            if not livre:
                print("Le livre spécifié n'existe pas et on renvoie le formulaire pour changer isbn")
            else:
                # cur = conn.cursor()
                # si la requête retourne un résultat nous mettons à jour les résultats
                cur.execute('UPDATE Livre SET titre = ?, auteur = ?, type = ? WHERE isbn = ?', (self.titre, self.auteur, self.type_livre, isbn))
                print("Mis à jour reussi")
            
            # conn.commit()
            # conn.close()
            

    def supprimer(self):
        # avant de supprimer un livre de la base on vérifie que l'utilisateur a bien le droit de 
        # le faire et que le livre existe bel et bien dans la base
        with conn:
            cur = conn.cursor()
            livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [self.isbn]).fetchone()

            if not livre:
                print(f"ISBN: {self.isbn} n'existe pas ")
            else:
                cur.execute('DELETE FROM Livre WHERE isbn = ?', (self.isbn,))
                conn.commit()
                print("Le livre a bien été supprimé")

            # conn.close()


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
        with conn:
            cur = conn.cursor()
            if param.lower() == 'isbn':
                if not cur.execute("SELECT * FROM Livre WHERE isbn like ?", (value,)).fetchone():
                    raise ValueError("Votre recherche n'a pas trouvé de correspondance")
                for row in cur.execute("SELECT * FROM Livre WHERE isbn like ?", (value,)):
                    print(f"""==================== RESULTAT DE VOTRE RECHERCHE ==========================
                            - Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})
                          """)
            elif param.lower() == 'titre':
                if not cur.execute("SELECT * FROM Livre WHERE titre like ?", (value.lower(),)).fetchone():
                    raise ValueError("Votre recherche n'a pas trouvé de correspondance")
                for row in cur.execute("SELECT * FROM Livre WHERE titre like ?", (value.lower(),)):
                    print(f"""==================== RESULTAT DE VOTRE RECHERCHE ==========================
                            - Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})
                          """)
            # Ausii faire un retour écran lorsqu'il n'y a pas de correspondance
            elif param.lower() == 'auteur':
                if not cur.execute("SELECT * FROM Livre WHERE auteur like ?", (value,)).fetchone():
                    raise ValueError("Votre recherche n'a pas trouvé de correspondance")
                for row in cur.execute("SELECT * FROM Livre WHERE auteur like ?", (value,)):
                    print(f"""==================== RESULTAT DE VOTRE RECHERCHE ==========================
                            - Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})
                          """)
            # conn.commit()
            # conn.close()

    def emprunter(self, isbn, emprunteur):
        # Avant de pouvoir emprunter un livre on doit vérifier qu'il est bien disponible
        with conn:
            cur = conn.cursor()
            livre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn and disponible = 1", [isbn]).fetchall()

            if not livre:
                print("Le livre n'est pas disponible ou isbn saisie est incorrect")
            else:
                # Si un résultat est retourné, on part l'élément afin de récupérer la clé nombre et ainsi l'incrémenter
                livre_dans_emprunt = cur.execute("SELECT * FROM Emprunt WHERE isbn LIKE :isbn", [isbn]).fetchall()
                if not livre_dans_emprunt:
                    cur.execute("INSERT INTO Emprunt VALUES(?, ?, ?)", (isbn, emprunteur, 1))
                else:
                    for row in livre_dans_emprunt:
                        # Avant d'insérer l'ISBN du livre emprunté dans la table "Emprunt", je vérifie en amont s'il n'existe pas déjà dans la base.
                        # Si c'est cas l'incrémente "nombre" de 1
                        # Sinon on l'ajoute, on met à jour
                        print(row[2])
                        cur.execute('UPDATE Emprunt SET nombre = ? WHERE isbn = ?', (int(row[2])+1, isbn))
                        # cur.execute("INSERT INTO Emprunt VALUES(?, ?, ?)", (isbn, emprunteur, int(row[4]) + 1))
                    
                # On met la valeur de disponible à faux vu celui-ci a été emprunté
                cur.execute('UPDATE Livre SET disponible = 0 WHERE isbn = ?', (isbn,))
            #conn.commit()
        #conn.close()

    def retourner(self, isbn):
        with conn:
            cur = conn.cursor()
            cur.execute('UPDATE Livre SET disponible = 1 WHERE isbn = ?', (isbn,))
        conn.close()


class LivrePapier(Livre):
    pass

class LivreNumerique(Livre):
    ...


if __name__ == '__main__':
    """ lister()
    statistiques() """
    livre = Livre("Moby Dick", "Herman Melville", "978-0-57-148410-7", "Papier")
    try:
        livre.ajouter()
        print("Le livre a bien été rajouté à la liste")
    except Exception as e:
        print(e)
    
    livre.rechercher('auteur', 'Émile Zola')
    """ livre.emprunter('978-1234567890', 'Antonin')
    livre.retourner('978-1234567890') """
    print('Tout es ok')
