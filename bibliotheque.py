import livre
import user
import db
class Bibliotheque:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.livres = []
            cls._instance.users = []
        return cls._instance
    
    def ajouter_un_livre(self, param: livre.Livre) -> bool:
        with db.conn:
            cur = db.conn.cursor()
            cur.execute("INSERT OR REPLACE INTO Livre VALUES(?, ?, ?, ?, ?)", (param.titre, param.auteur, param.isbn, param.type_livre.lower(), param.disponible))
    
    def ajouter_un_utilisateur(self, param: user.User):
        with db.conn:
            cur = db.conn.cursor()
            cur.execute("INSERT OR REPLACE INTO User VALUES(?, ?)", (param.nom, param.type_utilisateur))

    def afficher_les_livres(self) -> None:
        print("====================== LISTE DES LIVRES DISPONIBLES DANS LA BIBLIOTHEQUES ==============")
        with db.conn:
            cur = db.conn.cursor()
            for livre in cur.execute("SELECT titre, auteur, isbn, type_livre FROM Livre").fetchall():
                print(livre)
                self.livres.append(livre)
        print("=========================================================================================")
    
    def afficher_les_utilisateurs(self) -> None:
        print("====================== LISTE DES UTILISATEURS DISPONIBLES DANS LA BIBLIOTHEQUES ==============")
        with db.conn:
            cur = db.conn.cursor()
            for user in cur.execute("SELECT * FROM User").fetchall():
                print(user)
                self.users.append(user)
        print("=========================================================================================")

    def statistiques(self):
        with db.conn:
            cur = db.conn.cursor()
            # Nombre de livre dans la base
            nombre_de_livre = cur.execute('SELECT COUNT(*) FROM Livre').fetchone()
            # Nombre de livre emprunté
            nombre_de_livre_emprunte = cur.execute('SELECT COUNT(*) FROM Livre WHERE disponible is False').fetchone()
            # nombre total d'utilisateur
            nombre_d_utilisateur = cur.execute('SELECT COUNT(*) FROM User').fetchone()
            # Livres le plus emprunté
            # D'abord on vérifie que la table Emprunt n'est pas vide
            livre_emprunte = cur.execute('SELECT isbn FROM Emprunt').fetchone()

            if not livre_emprunte:
                livre_emprunte = "Pas de livres empruntés"
            else:
                livre_emprunte = cur.execute('SELECT isbn, nombre FROM Emprunt ORDER BY nombre DESC LIMIT 1').fetchone()

            resultat = f"""

            =============== QUELQUES STATISTIQUES =============================

                - Nombre de livre: {nombre_de_livre[0]}
                - Nombre total d'utilisateur: {nombre_d_utilisateur[0]}
                - Nombre de livre emprunté: {nombre_de_livre_emprunte[0]}
                - L'ISBN du livre le plus emprunté: {livre_emprunte}

            ==================================================================
    """
            
            
            return resultat

    def rechercher(self, param: str, value: str) -> None:

        # On permet à l'utlisateur de faire sa recherche avec ISBN ou le nom de l'auteur
        
        with db.conn:
            cur = db.conn.cursor()

            if param.lower() == 'isbn':
                print("========================== RESULTAT DE VOTRE RECHERCHE =========================")
                if not cur.execute("SELECT * FROM Livre WHERE isbn like ?", (value,)).fetchall():
                    print(" PAS DE RESULTAT")
                    print("=============================================================================")
                else:
                    for row in cur.execute("SELECT * FROM Livre WHERE isbn like ?", (value,)):
                        print(f"- Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})")
                    print("=============================================================================")

            # Ausii faire un retour écran lorsqu'il n'y a pas de correspondance
            elif param.lower() == 'auteur':

                print("========================== RESULTAT DE VOTRE RECHERCHE =========================")
                if not cur.execute("SELECT * FROM Livre WHERE auteur like ?", (value,)).fetchall():
                    print("PAS DE RESULTAT")
                    print("=============================================================================")
                else:
                    for row in cur.execute("SELECT * FROM Livre WHERE auteur like ?", (value,)):
                        print(f" - Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})")
                    print("=============================================================================")

    def emprunter_un_livre(self, isbn, emprunteur) -> bool:

        with db.conn:
            # Si un résultat est retourné, on part l'élément afin de récupérer la clé nombre et ainsi l'incrémenter
            cur = db.conn.cursor()
            livre_dans_emprunt = cur.execute("SELECT * FROM Emprunt WHERE isbn LIKE :isbn", [isbn]).fetchall()
            if not livre_dans_emprunt:
                cur.execute("INSERT INTO Emprunt VALUES(?, ?, ?)", (isbn, emprunteur, 1))
            else:
                for row in livre_dans_emprunt:
                    # Avant d'insérer l'ISBN du livre emprunté dans la table "Emprunt", je vérifie en amont s'il n'existe pas déjà dans la base.
                    # Si c'est cas l'incrémente "nombre" de 1
                    # Sinon on l'ajoute, on met à jour
                    cur.execute('UPDATE Emprunt SET nombre = ? WHERE isbn = ?', (int(row[2])+1, isbn))
                    cur.execute('UPDATE Emprunt SET emprunteur = ? WHERE isbn = ?', (emprunteur, isbn))
                    # cur.execute("INSERT INTO Emprunt VALUES(?, ?, ?)", (isbn, emprunteur, int(row[4]) + 1))
                
            # On met la valeur de disponible à faux vu celui-ci a été emprunté
            cur.execute('UPDATE Livre SET disponible = 0 WHERE isbn = ?', (isbn,))

        # Le return n'a d'utilité que pour les tests

    def retourner_un_livre(self, isbn: str, emprunteur: str):
        # Avant de pouvoir retourner un livre on doit vérifier qu'il a bien été emprunté
        with db.conn:
            cur = db.conn.cursor()
            livre_existe = cur.execute("SELECT isbn FROM Emprunt WHERE isbn LIKE :isbn and emprunteur LIKE :emprunteur ", [isbn, emprunteur]).fetchall()

            if not livre_existe:
                return "ISBN ou le nom de l'emprunteur saisie est incorrect"
            cur.execute('UPDATE Livre SET disponible = 1 WHERE isbn = ?', (isbn,))
            return "Votre retour a bien été pris en compte"


if __name__ == "__main__":
    bibliotheque = Bibliotheque()
    bibliotheque.afficher_les_utilisateurs()
    bibliotheque.statistiques()