from livre import Livre
from bibliotheque import Bibliotheque

def test_creation_livre():
    # Tester la création d'un objet Livre
    livre = Livre("Les Misérables", "Victor Hugo", "978-1234567890", "papier")
    assert livre.titre == "Les Misérables"
    assert livre.auteur == "Victor Hugo"
    assert livre.isbn == "978-1234567890"
    assert livre.type_livre == 'papier'
    assert livre.disponible == 1

def test_supprimer_un_livre():
    livre = Livre("Les Misérables", "Victor Hugo", "978-1234567890", "papier")
    bibliotheque = Bibliotheque()
    bibliotheque.ajouter_un_livre(livre)
    assert livre.supprimer() == "Le livre a bien été supprimé"

