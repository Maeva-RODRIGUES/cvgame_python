import json
from classes.platform import Platform
from classes.badge import Badge

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

    @property
    def number(self):
        """Numéro du niveau courant (1 pour level_1)."""
        return int(self.current_level.split("_")[1])

    @property
    def count(self):
        """Nombre total de niveaux."""
        return len(self.levels)

    @property
    def title(self):
        return self.levels[self.current_level]["title"]

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
            self.badges = [Badge(badge_pos["x"], badge_pos["y"], data["badge"])]

    def next_level(self):
        """Passe au niveau suivant"""
        next_level = f"level_{self.number + 1}"

        if next_level in self.levels:
            self.current_level = next_level
            self.load_level()
            return True
        return False
