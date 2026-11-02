import asyncio
import sys

# pygbag repère les paquets à charger dans le navigateur d'après les imports de main.py
import pygame  # noqa: F401

from classes.game import Game
from classes.level_data import LevelDataError


async def main():
    try:
        await Game().run()
    except LevelDataError as e:
        sys.exit(f"Erreur dans data/levels.json : {e}")


if __name__ == "__main__":
    # Même lancement sur ordinateur et dans le navigateur (pygbag exécute main.py)
    asyncio.run(main())
