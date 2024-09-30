# gestion de bibliothèque

Ce projet s'exécute dans le terminal

## Fichiers
Le projet contient plusieurs fichiers dont quatre principaux:

- main.py qui gère tout le fonctionnement de l'application
- livre.py contient l'implémentation de la classe Livre 
- db.py comme son nom l'indique, il contient tout le code qui concerne la création et l'insertion des données dans la base.
Pour avoir une base préremplie avec des données dans les différentes tables (Livre, User), il est recommander d'exécuter
ce fichier en premier.

J'ai opté pour l'insertion de 10 lignes dans la table "Livre" et 2 utulisateurs dans la table "User" de la base de données pour nos tests. 
L'utulisatuer pourra bien sûr par la suite ajouter plusieurs autres livres et users.

### Fonctionnement de l'application

Après avoir exécuté le fichier db.py necessaire à  la création de la base de données, on exécute le fichier main.py pour lancer l'application.

Attention!!!!! la création d'un utilisateur nécessite de spécifier de quel utulisateur s'agit-il.
- Un administrateur (admin) a tous les droits sur base et peux donc tout faire 
- Un étudiant a un accès restreint, il peut par exemple emprunter ou lister des livres, mais pas supprimer des livres.

Après avoir exécuter la fonction main.py, l'utulisateur a les choix suivants pour les gestion de la bibliotheque:

1. Il peut jouter un livre en spécifiant (le titre, l'auteur, l'isbn, le type du livre(papier/numerique))
2. Il peut supprimer un livre si son type est "admin"
3. Rechercher un livre par son ISBN ou le nom d'auteur
4. Ajouter un utlisateur
5. Emprunter un livre, sachant qu'un livre déjà emprunté ne plus être emprunté à nouveau à moins de le retourner et par la suite le réemprunter
6. Retourner un livre
7. Lister l'ensemble des livres contenues dans la base de données
8. Afficher quelques statistiques
9. QUITTER

## Base de données

3 tables dans la base;
- Livre (titre: str, auteur: str, isbn: str, type_livre: (papier, numerique), disponible: bool)
Lorsqu'un livre est emprunté la colonne disponible passe false permettant ainsi de plus le réemprunter
- User (nom, type_utulisateur (admin/etudiant))
- Emprunt (isbn: str, nombre: int)

la colonne "nombre" de la table Emprunt permet de savoir le nombre de fois q'un livre a été emprunté.
A chaque fois q'un même livre est emprunté, cette colonne est incrémentée de 1 s'il existe déjà dans table Emprunt.
Ceci permet tres facilement de récupérer par exemple ISBN du livre le plus emprunté.
