import sys

from classes.game import Game
from classes.level_data import LevelDataError

if __name__ == "__main__":
    try:
        Game().run()
    except LevelDataError as e:
        sys.exit(f"Erreur dans data/levels.json : {e}")
