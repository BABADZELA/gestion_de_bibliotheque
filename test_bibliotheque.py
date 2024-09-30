import pytest

from livre import Livre
from user import User
from bibliotheque import Bibliotheque
from db import conn

@pytest.fixture
def livre():
    return  Livre("Les Misérables", "Victor Hugo", "978-1234567890", "papier")

@pytest.fixture
def bibliotheque():
    return  Bibliotheque()

@pytest.fixture
def utulisateur():
    return  User('Christopher', 'Admin')

def test_ajouter_un_livre(livre, bibliotheque):
    bibliotheque.ajouter_un_livre(livre)
    with conn:
        cur = conn.cursor()
        assert  (livre.isbn,) in cur.execute("SELECT isbn FROM Livre").fetchall()


def test_afficher_les_livres(bibliotheque):
    with conn:
        cur = conn.cursor()
        bibliotheque.afficher_les_livres()
        assert bibliotheque.livres == cur.execute("SELECT titre, auteur, isbn, type_livre FROM Livre").fetchall()

def test_afficher_les_utilisateurs(bibliotheque):
    with conn:
        cur = conn.cursor()
        bibliotheque.afficher_les_utilisateurs()
        assert bibliotheque.users == cur.execute("SELECT * FROM User").fetchall()


def test_ajouter_les_utilisateurs(bibliotheque, utulisateur):
    bibliotheque.ajouter_un_utilisateur(utulisateur)
    with conn:
        cur = conn.cursor()
        assert (utulisateur.nom,) in cur.execute("SELECT nom FROM User").fetchall()


def test_emprunter_un_livre(livre, bibliotheque, utulisateur):
    bibliotheque.emprunter_un_livre(livre.isbn, utulisateur.nom)

    with conn:
        cur = conn.cursor()
        assert (livre.isbn,) in cur.execute("SELECT isbn FROM Emprunt").fetchall()


def test_retourner_un_livre(livre, bibliotheque, utulisateur):
    bibliotheque.emprunter_un_livre(livre.isbn, utulisateur.nom)
    bibliotheque.retourner_un_livre(livre.isbn, utulisateur.nom)

    assert livre.disponible == 1
    



