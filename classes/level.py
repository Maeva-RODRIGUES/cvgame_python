import json
from classes.platform import Platform

class LevelManager:
    def __init__(self, json_path):
        # data/levels.json : source unique (titre, dialogue, badge, plateformes...)
        with open(json_path, "r", encoding="utf-8") as f:
            self.levels = json.load(f)

        self.current_level = "level_1"
        self.platforms = []
        self.badges = []
        self.width = 0
        self.load_level()

    def load_level(self):
        """Charge les données du niveau actuel"""
        data = self.levels.get(self.current_level, {})

        # Largeur du niveau en pixels (bornes de la caméra et du joueur)
        self.width = data["width"]

        # Charger les plateformes
        self.platforms = [Platform(p["x"], p["y"], p["width"]) for p in data.get("platforms", [])]

        # Badge du niveau : type + position (un seul par niveau)
        badge_pos = data.get("badge_pos")
        self.badges = []
        if badge_pos:
            self.badges = [{"x": badge_pos["x"], "y": badge_pos["y"], "type": data["badge"]}]

    def next_level(self):
        """Passe au niveau suivant"""
        level_number = int(self.current_level.split("_")[1])
        next_level = f"level_{level_number + 1}"

        if next_level in self.levels:
            self.current_level = next_level
            self.load_level()
            return True
        return False
