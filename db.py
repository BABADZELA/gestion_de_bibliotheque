import sqlite3


conn = sqlite3.connect("bibliotheque.db")
cur = conn.cursor()

# Créer une table 'user' dans la base de données SQLite qui contiendra les users
cur.execute('''
    CREATE TABLE IF NOT EXISTS User (
        nom TEXT NOT NULL UNIQUE,
        type_utilisateur VARCHAR(50) NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Emprunt (
        isbn TEXT NOT NULL UNIQUE,
        emprunteur VARCHAR(50) NOT NULL,
        nombre INTEGER DEFAULT 0
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Livre (
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL,
        isbn TEXT NOT NULL UNIQUE,
        type VARCHAR(50) NOT NULL,
        disponible BOOLEAN NOT NULL CHECK (disponible IN (0, 1))
    )
''')

if __name__ == '__main__':

    livres = [
    ("Les Misérables","Victor Hugo","978-1234567890","papier", 1),
    ("Le Petit Prince","Antoine de Saint-Exupéry","978-9876543210", "numérique", 1),
    ("L'Étranger","Albert Camus","978-1122334455", "papier", 1),
    ("À la recherche du temps perdu","Marcel Proust","978-9988776655", "numérique", 1),
    ("Le Rouge et le Noir","Stendhal","978-6677889900", "papier", 1),
    ("Madame Bovary","Gustave Flaubert","978-5566778899", "papier", 1),
    ("Le Comte de Monte-Cristo","Alexandre Dumas","978-3344556677", "numérique", 1),
    ("Germinal","Émile Zola","978-4455667788", "papier", 1),
    ("Les Fleurs du mal","Charles Baudelaire","978-2233445566", "papier", 1),
    ("Don Quichotte","Miguel de Cervantes","978-3322114455", "numérique", 1)
]
    
    users = [
        ("John","etudiant"),
        ("Glory","admin"),
    ]
    
    # Insertion des données dans la base de données
    cur.executemany("INSERT INTO Livre VALUES(:titre, :auteur, :isbn, :type, :disponible)", livres)
    cur.executemany("INSERT INTO User VALUES(:nom, :type_utilisateur)", users)

    conn.commit()
    conn.close()