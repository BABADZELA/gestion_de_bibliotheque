import livre
import user
import db


class Bibliotheque:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            with db.conn:
                cur = db.conn.cursor()
                cls._instance.livres = cur.execute("SELECT * FROM Livre").fetchall()
                cls._instance.users = cur.execute("SELECT * FROM User").fetchall()
            # db.conn.close()
        return cls._instance
    
    def ajouter_un_livre(self, param: livre) -> None:
        with db.conn:
            cur = db.conn.cursor()
            cur.execute("INSERT INTO Livre VALUES(?, ?, ?, ?, ?)", (param.titre, param.auteur, param.isbn, param.type_livre.lower(), param.disponible))

    def afficher_les_livres(self) -> None:
        print("====================== LISTE DES LIVRES DISPONIBLES DANS LA BIBLIOTHEQUES ==============")
        for livre in self.livres:
            print(livre)
        print("=========================================================================================")
    
    def afficher_les_utilisateurs(self) -> None:
        print("====================== LISTE DES LIVRES DISPONIBLES DANS LA BIBLIOTHEQUES ==============")
        for user in self.users:
            print(user)
        print("=========================================================================================")

    def statistiques(self):
        with db.conn:
            cur = db.conn.cursor()
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
                livre_emprunte = cur.execute('SELECT isbn, nombre FROM Emprunt ORDER BY nombre DESC LIMIT 1').fetchone()

            resultat = f"""

            =============== QUELQUES STATISTIQUES =============================

                - Nombre de livre: {nombre_de_livre[0]}
                - Nombre total d'utilisateur: {nombre_d_utilisateur[0]}
                - Nombre de livre emprunté: {nombre_de_livre_emprunté[0]}
                - L'ISBN du livre le plus emprunté: {livre_emprunte}

            ==================================================================
    """
            
            
            print(resultat)

    def rechercher(self, param: str, value: str) -> None:

        # On permet à l'utlisateur de faire sa recherche avec ISBN ou le nom de l'auteur
        
        with db.conn:
            cur = db.conn.cursor()

            print("========================== RESULTAT DE VOTRE RECHERCHE =========================")
            if param.lower() == 'isbn':
                for row in cur.execute("SELECT * FROM Livre WHERE isbn like ?", (value,)):
                    print(f"- Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})")

            # Ausii faire un retour écran lorsqu'il n'y a pas de correspondance
            elif param.lower() == 'auteur':

                print("========================== RESULTAT DE VOTRE RECHERCHE =========================")
                for row in cur.execute("SELECT * FROM Livre WHERE auteur like ?", (value,)):
                    print(f" - Livre: {row[0]}, écrit par: {row[1]}, (ISBN: {row[2]}, Type de livre: {row[3]})")


if __name__ == "__main__":
    bibliotheque = Bibliotheque()
    bibliotheque.afficher_les_utilisateurs()
    bibliotheque.statistiques()