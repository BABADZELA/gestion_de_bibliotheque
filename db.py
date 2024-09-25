import sqlite3


conn = sqlite3.connect("user.db")
cur = conn.cursor()


data = [
    ("Les Misérables","Victor Hugo","978-1234567890","papier"),
    ("Le Petit Prince","Antoine de Saint-Exupéry","978-9876543210", "numérique"),
    ("L'Étranger","Albert Camus","978-1122334455", "papier"),
    ("À la recherche du temps perdu","Marcel Proust","978-9988776655", "numérique"),
    ("Le Rouge et le Noir","Stendhal","978-6677889900", "papier"),
    ("Madame Bovary","Gustave Flaubert","978-5566778899", "papier"),
    ("Le Comte de Monte-Cristo","Alexandre Dumas","978-3344556677", "numérique"),
    ("Germinal","Émile Zola","978-4455667788", "papier"),
    ("Les Fleurs du mal","Charles Baudelaire","978-2233445566", "papier"),
    ("Don Quichotte","Miguel de Cervantes","978-3322114455", "numérique")
]

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
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Livre (
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL,
        isbn TEXT NOT NULL UNIQUE,
        type VARCHAR(50) NOT NULL,
        disponible BOOLEAN NOT NULL DEFAULT TRUE,
    )
''')



# Insertion des données dans la base de données SQLite
# cur.executemany("INSERT INTO Livre VALUES(:titre, :auteur, :isbn, :type)", data)

#conn.commit()
#conn.close()

if __name__ == '__main__':
    conn = sqlite3.connect("user.db")
    cur = conn.cursor()
    isbn = input("ISBN: ")

    nombre = cur.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [isbn]).fetchall()

    if not nombre:
        print("Liste vide")

    print(nombre)

    for row in conn.execute("SELECT * FROM Livre WHERE isbn LIKE :isbn", [isbn]):
        print(row)
    

    
    conn.close()