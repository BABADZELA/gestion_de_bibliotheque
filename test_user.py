from user import User


def test_creation_user():
    utulisateur = User("Christopher", "Admin")

    assert utulisateur.nom == "Christopher"
    assert utulisateur.type_utilisateur == "admin"
    assert utulisateur.__str__() == "Christopher:admin"

