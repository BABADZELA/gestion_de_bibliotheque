# gestion de bibliothèque

Ce projet s'exécute dans le terminal

## Fichiers
J'ai découpé le projet en trois ficheirs afin de séparer les fonctionnalités.

Le projet contient 3 fichiers python:
- main qui gère tout le fonctionnement de l'application
- livre contient l'implémentation de la classe Livre 
- db comme son nom l'indique, il contient tout le code concernant la création et l'insertion des données dans la base.

J'ai opté pour l'insertion de 10 lignes dans la base de données pour nos tests. 
L'utilisatuer pourra bien sur par la suite ajouter plusieurs autres livre.

### Fonctionnement de l'application

L'utilisateur doit au préalable se connecter un utilisateur en spécifiant s'il s'agit d'un administrateur ou d'un étudiant.
- Un administrateur peut ajouter et supprimer des livres 
- Un étudiant peut emprunter ou lister des livres.


## Statistique
Pour les besoins de statistique j'ai rajouté la table emprunt qui contient 2 champs:
- isbn
- nombre de fois que celui-ci a été emprunté
- user qui emprunte le livre

Une fois qu'un livre est emprunté, celui-ci est stocké dans cette table. S'il est emprunté encore une fois,
la colonne nombre est incrémentée de 1. isbn contenant le nombre le plus élevé sera le livre le plus emprunté.

## Base de données

3 tables pour l'instant dans la base;
- Livre
- User
- Emprunt


la table emprunt se remplit automatiquement lorsque qu'un livre est emprunté 

Dans la table Livre j'ai rajouté la colonne disponibible qui me permet de stocker
un booléan pour savoir si un livre peut être emprunté ou pas 

### Utilisation
La base a déjà été créer ainsi que les tables. Les d'insertions des données dans la base ont
donc été commentées afin d'éviter les erreurs.

Tel que codé l'emprunteur doit obligatoirement être un user de type "étudiant"
### Piste d'amélioration

Pour la saisie du nom de l'utlisation dans le terminal je n'ai pas tenu compte des cas ou l'utilisateur 
saisie des caractères spéciaux