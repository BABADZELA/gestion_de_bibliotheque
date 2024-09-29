from livre import Livre

def test_creation_livre():
    # Tester la création d'un objet Livre
    livre = Livre("Les Misérables", "Victor Hugo", "978-1234567890", "papier")
    assert livre.titre == "Les Misérables"
    assert livre.auteur == "Victor Hugo"
    assert livre.isbn == "978-1234567890"
    assert livre.type_livre == 'papier'
    assert livre.disponible == 1