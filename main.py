import logging
import typer
from typing import Optional
from pathlib import Path
import sqlite3


import livre, user, db, bibliotheque

# app = typer.Typer()

import emoji

def temp_emprunt():
    isbn = input("Entrez l'ISBN du livre à emprunter: ")
    # Avant de pouvoir emprunter un livre on doit vérifier qu'il est bien disponible
    with db.conn:
        cur = db.conn.cursor()
        livre_existe = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn and disponible = 1", [isbn]).fetchall()

        if not livre_existe:
            typer.secho("Le livre n'est pas disponible ou isbn saisie est incorrect", fg='red')
        else:
            for row in livre_existe:
                test = livre.Livre(row[0], row[1], row[2], row[3])
            test.emprunter(isbn, emprunter)

            typer.secho("Le livre a bien été emprunté", fg='green')

choices_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

choices = ["Ajouter un livre", "Supprimer un livre", "Rechercher un livre", "Ajouter un utlisateur", "Emprunter un livre",
"Retourner un livre", "Lister les livres", "Statistiques", "QUITTER"]

emoji_p = emoji.emojize(":thumbs_up:", language='alias')

# Afficher la liste des choix
typer.echo("GESTION DE BIBLIOTHEQUE")
for index, choice in enumerate(choices, start=1):
    typer.echo(f"{index}. {choice}")
choix = typer.prompt("Choisissez un livre en entrant son numéro", type=str)

# choix = input(f"Veuillez choisir un chiffre parmi la liste ci-dessus {emoji_p} ")

def get_message() -> str:
    # typer.secho(message_a_affichager, fg=typer.colors.GREEN)
    # Afficher la liste des choix
    typer.echo("GESTION DE BIBLIOTHEQUE")
    for index, choice in enumerate(choices, start=1):
        typer.echo(f"{index}. {choice}")
    choix = typer.prompt("Choisissez un livre en entrant son numéro", type=str)
    # choix = input(f"Veuillez choisir un chiffre parmi la liste ci-dessus {emoji_p} ")
    return choix


# on vérifie que l'utilisateur saisie bien les valeurs indiquées sur la liste et rien d'autre
while choix not in choices_number:
    choix = get_message()

# Tant que l'utlisateur ne saisie pas la valeur 9, on continue à lui proposer la liste
while choix != '9':

    if choix == '1':
        titre = input("Veuillez saisir le titre du livre : ").lower()
        auteur = input("Veuillez saisir l'auteur du livre : ").lower()
        isbn = input("Veuillez saisir l'ISBN du livre : ").lower()

        with db.conn:
            cur = db.conn.cursor()
            while (isbn,) in cur.execute("SELECT isbn FROM Livre WHERE isbn LIke ?", (isbn,)).fetchall():
                typer.secho("L'ISBN saisie existe déjà dans la base", fg="red")
                isbn = input("Veuillez saisir l'ISBN du livre : ").lower()

        type_livre = input("Veuillez saisir le type du livre (papier / numerique) : ").lower()

        while type_livre not in ['papier', 'numerique']:
            type_livre = input("Veuillez saisir le type du livre (papier / numerique) : ").lower()

        nouveau_livre = livre.Livre(titre, auteur, isbn, type_livre)

        # Ajout du livre dans la base
        bibliotheque.Bibliotheque().ajouter_un_livre(nouveau_livre)

        typer.secho(f"{livre.Livre(titre, auteur, isbn, type_livre)} a bien été rajouté dans la base", fg="green") 

    elif choix == '2':
        # Avant de supprimer un livre, on vérifie que cet utulisateur a bien les droits de suppression
        nom_utulisateur = input("Utulisateur : ").lower()
        isbn = input("Entrez l'ISBN du livre à supprimer : ")
        with db.conn:
            cur = db.conn.cursor()
            nom_dans_base = cur.execute("SELECT * FROM User WHERE nom LIKE ?", (nom_utulisateur,)).fetchone()
            if not nom_dans_base:
                typer.secho(f"L'utulisateur: {nom_utulisateur} n'existe pas, veuillez d'abord l'ajouter", fg='red')
            else:
                # cet utilisateur existe, on vérifie donc qu'il ne s'agit pas d'un étudiant
                nom, type_utulisateur = nom_dans_base
                if type_utulisateur == 'etudiant':
                    typer.secho(f"L'utulisateur: {nom_utulisateur} n'a pas de droit de suppression ", fg='red')
                else:

                    cur = db.conn.cursor()
                    livre_existe = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn ", [isbn]).fetchall()

                    if not livre_existe:
                        typer.secho("L'ISBN du livre que vous souhaitez supprimer n'existe pas", fg='red')
                    else:
                        for row in livre_existe:
                            test = livre.Livre(row[0], row[1], row[2], row[3])
                        
                        confirm = typer.confirm(f"Souhaitez-vous vraiment supprimer le livre trouvé ?")

                        if confirm:
                            suppression = test.supprimer()
                            typer.secho(suppression, fg='green')
                        else:
                            typer.secho("Action de suppression annulée", fg='red')

    elif choix == '3':
        saisie = input("Comment souhaitez-vous réaliser votre recherche : (isbn / auteur) ").lower()

        while saisie not in ['isbn', 'auteur']:
            saisie = input("ISBN / Auteur)").lower()

        if saisie == 'isbn':
            isbn = input("Entrez l'ISBN: ")
        else:
            auteur = input("Entrez le nom de l'auteur: ")

        with db.conn:
            cur = db.conn.cursor()

            if saisie == 'isbn':
                bibliotheque.Bibliotheque().rechercher(saisie, isbn)
            else:
                bibliotheque.Bibliotheque().rechercher(saisie, auteur)
        

    elif choix == '4':
        nom_utulisateur = input("Utulisateur: ").lower()

        with db.conn:
            cur = db.conn.cursor()
            nom_dans_base = cur.execute("SELECT nom FROM User WHERE nom LIKE ?", (nom_utulisateur,)).fetchall()
            # On vérifie que le prénom saisie par l'utulisateur ne se trouve pas déjà dans la base
            # Si c'est le cas on redemande de saisir une nouvelle valeur
            while nom_dans_base:
                typer.secho(f"L'utulisateur': {nom_utulisateur} est déjà utilisé", fg='red')
                nom_utulisateur = input("Veuillez saisir un autre nom : ").lower()
                nom_dans_base = cur.execute("SELECT nom FROM User WHERE nom LIKE ?", (nom_utulisateur,)).fetchall()

        type_utulisateur = input("type d'utulisateur: (admin / etudiant) ").lower()

        # Que deux choix possibles à l'utulisateur
        while type_utulisateur not in ['admin', 'etudiant']:
            type_utulisateur = input("type d'utulisateur: (admin / etudiant) ")

        # Tout est ok, on insert l'utulisateur dans la base
        with db.conn:
            cur = db.conn.cursor()
            cur.execute("INSERT INTO User (nom, type_utilisateur) VALUES (?, ?)", (nom_utulisateur, type_utulisateur))

        typer.secho(f"L'utulisateur: {nom_utulisateur} a bien été ajouté", fg='green')

    elif choix == '5':
        # Avant de pouvoir emprunter un livre, on vérifie d'abord que l'emprunteur se trouve
        # bel et bien dans la table User
        emprunter = input("Nom de l'emprunteur du livre: ").lower()
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
                    type_utulisateur = input("type d'utulisateur: (admin / etudiant) ")
                    while type_utulisateur not in ['admin', 'etudiant']:
                        type_utulisateur = input("type d'utulisateur: (admin / etudiant) ")
                    
                    # Tout est ok, on insert le nouvel utulusateur dans la base
                    with db.conn:
                        cur = db.conn.cursor()
                        cur.execute("INSERT INTO User (nom, type_utilisateur) VALUES (?, ?)", (emprunter, type_utulisateur))

                    typer.secho(f"L'utulisateur: {emprunter} a bien été ajouté", fg='green')

                    temp_emprunt()


            else:

                temp_emprunt()
                

    elif choix == '6':
        isbn = input("Entrez l'ISBN du livre à retourner : ")
        emprunteur = input("Entrez le nom de l'emprunteur: ").lower()
        # Avant de pouvoir emprunter un livre on doit vérifier qu'il est bien disponible
        with db.conn:
            cur = db.conn.cursor()
            livre_existe = cur.execute("SELECT isbn FROM Emprunt WHERE isbn LIKE :isbn and emprunteur LIKE :emprunteur ", [isbn, emprunteur]).fetchall()

            if not livre_existe:
                typer.secho("ISBN ou le nom de l'emprunteur saisie est incorrect", fg='red')
            else:
                cur.execute('UPDATE Livre SET disponible = 1 WHERE isbn = ?', (isbn,))
                typer.secho("Votre retour a bien été pris en compte", fg='blue')

    elif choix == '7':
        bibliotheque.Bibliotheque().afficher_les_livres()
    
    else: 
        bibliotheque.Bibliotheque().statistiques()

    choix = get_message()

db.conn.close()



    
print("cest okay")
