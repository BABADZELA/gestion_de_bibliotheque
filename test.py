import typer

def main():
    # Liste des livres
    livres = [
        "1984 - George Orwell",
        "Le Meilleur des Mondes - Aldous Huxley",
        "Fahrenheit 451 - Ray Bradbury",
        "Dune - Frank Herbert",
        "Neuromancien - William Gibson"
    ]

    # Afficher les livres avec des numéros
    typer.echo("Liste des livres disponibles :")
    for index, livre in enumerate(livres, start=1):
        typer.echo(f"{index}. {livre}")

    # Demander à l'utilisateur de choisir un numéro
    while True:
        try:
            choix = typer.prompt("Choisissez un livre en entrant son numéro", type=int)
            if 1 <= choix <= len(livres):
                selection = livres[choix - 1]
                typer.echo(f"Vous avez choisi : {selection}")
                break
            else:
                typer.echo("Veuillez entrer un numéro valide.")
        except ValueError:
            typer.echo("Veuillez entrer un numéro valide.")

if __name__ == "__main__":
    typer.run(main)
