import json
from classes.platform import Platform

class LevelManager:
    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.levels = json.load(f)

        self.current_level = "level_1"
        self.platforms = []
        self.badges = []
        self.load_level()

    def load_level(self):
        """Charge les données du niveau actuel"""
        data = self.levels.get(self.current_level, {})

        # Charger les plateformes
        self.platforms = [Platform(y_pos=p["y"]) for p in data.get("platforms", [])]

        # Charger les badges
        self.badges = data.get("badges", [])

    def next_level(self):
        """Passe au niveau suivant"""
        level_number = int(self.current_level.split("_")[1])
        next_level = f"level_{level_number + 1}"

        if next_level in self.levels:
            self.current_level = next_level
            self.load_level()
            return True
        return False
