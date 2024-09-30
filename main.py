import typer
import emoji

import livre, db, bibliotheque, user

def temp_emprunt(emprunter):
    isbn = typer.prompt("Entrez l'ISBN du livre à emprunter: ")
    # Avant de pouvoir emprunter un livre on doit vérifier qu'il est bien disponible
    with db.conn:
        cur = db.conn.cursor()
        livre_disponible = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn and disponible = 1", [isbn]).fetchall()

        if not livre_disponible:
            typer.secho("Le livre n'est pas disponible ou isbn saisie est incorrect", fg='red')
        else:
            for row in livre_disponible:
                livre_temp = livre.Livre(row[0], row[1], row[2], row[3])

            bibliotheque.Bibliotheque().emprunter_un_livre(livre_temp.isbn, emprunter)
            # test.emprunter(isbn, emprunter)

            typer.secho("Le livre a bien été emprunté", fg='green')

choices_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

choices = ["Ajouter un livre", "Supprimer un livre", "Rechercher un livre", "Ajouter un utlisateur", "Emprunter un livre",
"Retourner un livre", "Lister les livres", "Statistiques", "QUITTER"]

emoji_p = emoji.emojize(":thumbs_up:", language='alias')

# Afficher la liste des choix
typer.echo("GESTION DE BIBLIOTHEQUE")
for index, choice in enumerate(choices, start=1):
    typer.echo(f"{index}. {choice}")
choix = typer.prompt(f"Veuillez choisir un chiffre parmi la liste ci-dessus {emoji_p}", type=str)

def get_message() -> str:
    # Afficher la liste des choix
    typer.echo("GESTION DE BIBLIOTHEQUE")
    for index, choice in enumerate(choices, start=1):
        typer.echo(f"{index}. {choice}")
    choix = typer.prompt(f"Veuillez choisir un chiffre parmi la liste ci-dessus {emoji_p}", type=str)
    return choix


# on vérifie que l'utilisateur saisie bien les valeurs indiquées sur la liste et rien d'autre
while choix not in choices_number:
    choix = get_message()

# Tant que l'utlisateur ne saisie pas la valeur 9, on continue à lui proposer la liste
while choix != '9':

    if choix == '1':
        ## On récupère tous les parametres necessaires à la création d'un livre
        titre = typer.prompt("Veuillez saisir le titre du livre ").lower()
        auteur = typer.prompt("Veuillez saisir l'auteur du livre ").lower()
        isbn = typer.prompt("Veuillez saisir l'ISBN du livre ").lower()

        with db.conn:
            cur = db.conn.cursor()
            #### Tant que l'isbn saisie est déjà dans la base, on redemande à l'utulisateur de saisir une nouvelle valeur
            while (isbn,) in cur.execute("SELECT isbn FROM Livre WHERE isbn LIke ?", (isbn,)).fetchall():
                typer.secho("L'ISBN saisie existe déjà dans la base", fg="red")
                isbn = typer.prompt("Veuillez saisir l'ISBN du livre ").lower()

        type_livre = typer.prompt("Veuillez saisir le type du livre (papier / numerique) ", type=str).lower()

        while type_livre not in ['papier', 'numerique']:
            type_livre = typer.prompt("Veuillez saisir le type du livre (papier / numerique) ", type=str).lower()

        nouveau_livre = livre.Livre(titre, auteur, isbn, type_livre)

        # Ajout du livre dans la base
        bibliotheque.Bibliotheque().ajouter_un_livre(nouveau_livre)

        typer.secho(f"{livre.Livre(titre, auteur, isbn, type_livre)} a bien été rajouté dans la base", fg="green") 

    elif choix == '2':
        # Avant de supprimer un livre, on vérifie que cet utulisateur a bien les droits de suppression
        nom_utulisateur = typer.prompt("Utulisateur ").lower()
        isbn = typer.prompt("Entrez l'ISBN du livre à supprimer ")
        with db.conn:
            cur = db.conn.cursor()
            ### On qu'il existe bien un utulisateur dans la base user correspondant à la saisie de l'utulisateur
            nom_dans_base = cur.execute("SELECT * FROM User WHERE nom LIKE ?", (nom_utulisateur,)).fetchone()
            if not nom_dans_base:
                typer.secho(f"L'utulisateur: {nom_utulisateur} n'existe pas, veuillez d'abord l'ajouter", fg='red')
            else:
                # Si utilisateur existe, on vérifie qu'il ne s'agit pas d'un étudiant
                nom, type_utulisateur = nom_dans_base
                if type_utulisateur == 'etudiant':
                    typer.secho(f"L'utulisateur: {nom_utulisateur} n'a pas de droit de suppression ", fg='red')
                else:

                    cur = db.conn.cursor()
                    livre_existe = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn ", [isbn]).fetchall()

                    ### On vérifie qu'il existe bien un livre dans base avec ISBN saisie par l'utulisateur
                    if not livre_existe:
                        typer.secho("L'ISBN du livre que vous souhaitez supprimer n'existe pas", fg='red')
                    else:
                        ## Le livre existe, on le recree et on le stocke dans la variable test
                        for row in livre_existe:
                            test = livre.Livre(row[0], row[1], row[2], row[3])
                        
                        confirm = typer.confirm(f"Souhaitez-vous vraiment supprimer le livre trouvé ?")

                        if confirm:
                            ########## Suppression du livre
                            suppression = test.supprimer()
                            typer.secho(suppression, fg='green')
                        else:
                            typer.secho("Action de suppression annulée", fg='red')

    elif choix == '3':
        saisie = typer.prompt("Comment souhaitez-vous réaliser votre recherche : (isbn / auteur) ").lower()

        while saisie not in ['isbn', 'auteur']:
            saisie = typer.prompt("(ISBN / Auteur)", type=str).lower()

        if saisie == 'isbn':
            isbn = typer.prompt("Entrez l'ISBN: ", type=str)
        else:
            auteur = typer.prompt("Entrez le nom de l'auteur: ", type=str)

        with db.conn:
            cur = db.conn.cursor()

            if saisie == 'isbn':
                bibliotheque.Bibliotheque().rechercher(saisie, isbn)
            else:
                bibliotheque.Bibliotheque().rechercher(saisie, auteur)
        

    elif choix == '4':
        nom_utulisateur = typer.prompt("Utulisateur: ").lower()

        with db.conn:
            cur = db.conn.cursor()
            nom_dans_base = cur.execute("SELECT nom FROM User WHERE nom LIKE ?", (nom_utulisateur,)).fetchall()
            # On vérifie que le prénom saisie par l'utulisateur ne se trouve pas déjà dans la base
            # Si c'est le cas on lui redemande de saisir une nouvelle valeur
            while nom_dans_base:
                typer.secho(f"L'utulisateur': {nom_utulisateur} est déjà utilisé", fg='red')
                nom_utulisateur = typer.prompt("Veuillez saisir un autre nom ", type=str).lower()
                nom_dans_base = cur.execute("SELECT nom FROM User WHERE nom LIKE ?", (nom_utulisateur,)).fetchall()

        # Entrer le type d'utulisateur (admin ou etudiant sans accent)
        type_utulisateur = typer.prompt("type d'utulisateur: (admin / etudiant) ", type=str).lower()

        # Que deux choix possibles à l'utulisateur
        while type_utulisateur not in ['admin', 'etudiant']:
            type_utulisateur = typer.prompt("type d'utulisateur: (admin / etudiant) ")

        # Tout est ok, on insert l'utulisateur dans la base
        with db.conn:
            cur = db.conn.cursor()
            cur.execute("INSERT INTO User (nom, type_utilisateur) VALUES (?, ?)", (nom_utulisateur, type_utulisateur))

        typer.secho(f"L'utulisateur: {nom_utulisateur} a bien été ajouté", fg='green')

    elif choix == '5':
        # Avant de pouvoir emprunter un livre, on vérifie d'abord que l'emprunteur se trouve
        # bel et bien dans la table User
        emprunter = typer.prompt("Nom de l'emprunteur du livre ", type=str).lower()
        with db.conn:
            cur = db.conn.cursor()
            nom_dans_base = cur.execute("SELECT nom FROM User WHERE nom LIKE ?", (emprunter,)).fetchall()

            # si l'utlisateur n'est pas dans la base, on lui propose de l'ajouter
            if not nom_dans_base:
                typer.secho(f"L'emprunteur': {emprunter} n'est pas un utilisateur", fg='red')

                confirmation = typer.confirm(f"Souhaitez-vous l'ajouter ? ")

                if not confirmation:
                    typer.secho("action annulée", fg='red')
                    
                else:
                    ######### Après avoir insérer cet utulisateur, on continue le processus d'emprunt avec la demande du type d'utulisateur
                    type_utulisateur = typer.prompt("type d'utulisateur: (admin / etudiant) ")
                    while type_utulisateur not in ['admin', 'etudiant']:
                        type_utulisateur = typer.prompt("type d'utulisateur: (admin / etudiant) ")
                    
                    # Tout est ok, on insert le nouvel utulusateur dans la base
                    with db.conn:
                        cur = db.conn.cursor()
                        cur.execute("INSERT INTO User (nom, type_utilisateur) VALUES (?, ?)", (emprunter, type_utulisateur))

                    typer.secho(f"L'utulisateur: {emprunter} a bien été ajouté", fg='green')

                    temp_emprunt(emprunter)


            else:

                temp_emprunt(emprunter)
                

    elif choix == '6':
        isbn = typer.prompt("Entrez l'ISBN du livre à retourner ", type=str)
        emprunteur = typer.prompt("Entrez le nom de l'emprunteur ", type=str).lower()

        retour = bibliotheque.Bibliotheque().retourner_un_livre(isbn, emprunteur)
        typer.secho("Votre retour a bien été pris en compte", fg='blue')

    elif choix == '7':
        bibliotheque.Bibliotheque().afficher_les_livres()
    
    elif choix == '8':
        resultat = bibliotheque.Bibliotheque().statistiques()
        typer.secho(resultat, fg='green')

    choix = get_message()

db.conn.close()



    
print("TERMINE")
