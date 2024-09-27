import logging
import typer
from typing import Optional
from pathlib import Path

app = typer.Typer()

logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
                    filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf8')



logging.debug("La foncction a bien été exécutée")
logging.info("Message d'information général")
logging.warning("attention !")
logging.error("Une erreur est arrivée")
logging.critical("Erreur critique")


@app.command("run")
def main_projet(extension: str,
                directory: Optional[str] = typer.Argument(None, help="Dossier dans lequel chercher"),
                delete: bool = typer.Option(False, help="Supprime les fichiers trouvés")):
    """ Ce projet affiche toutes les extensions trouvées dans les différents dossiers"""
    
    if directory: 
        directory = Path(directory)
    else:
        # on récupère le chemin courant lorsqu'un chemin n'est pas defini
        directory = Path.cwd()
    # print(directory)

    # On vérifie si le dossier spécifier existe belle et bien 
    if not directory.exists():
        typer.secho(f"Le dossier '{directory}' n'existe pas.", fg=typer.colors.RED)
        raise typer.Exit()
    
    # rglob permet de chercher dans un dossier de manière récurcive sur un objet de type Path
    files = directory.rglob(f"*.{extension}")
    if delete:
        typer.confirm(f"Souhaitez-vous vraiment supprimer tous les fichiers trouvés ?", abort=True)
        for file in files:
            # unclick permet de supprimer les fichiers sur le disque
            file.unlink()
            typer.secho(f"Suppression du fichier {file}", fg=typer.colors.RED)
    else:
        for file in files:
            typer.secho(f" {file}", fg=typer.colors.GREEN)

@app.command()
def search(extension: str):
    main_projet(extension=extension, directory=None, delete=False)

@app.command()
def delete(extension: str):
    main_projet(extension=extension, directory=None, delete=True)

if __name__ == '__main__':
    # typer.run(main_projet)
    app()