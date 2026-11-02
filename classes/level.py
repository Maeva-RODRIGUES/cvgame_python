from classes.level_data import load_levels
from classes.platform import Platform
from classes.badge import Badge, FinalFlag
from settings import BADGE_SIZE, FINAL_BADGE

class LevelManager:
    def __init__(self, json_path):
        # data/levels.json : source unique, validée au chargement (voir level_data.py)
        self.levels = load_levels(json_path)

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
        return self.levels[self.current_level].title

    def load_level(self):
        """Charge les données du niveau actuel"""
        data = self.levels[self.current_level]

        # Largeur du niveau en pixels (bornes de la caméra et du joueur)
        self.width = data.width

        # Charger les plateformes
        self.platforms = [Platform(p.x, p.y, p.width) for p in data.platforms]

        # Badge du niveau : type + position (un seul par niveau)
        if data.badge == FINAL_BADGE:
            self.badges = [self._final_flag(data.badge_pos, data.badge)]
        else:
            self.badges = [Badge(data.badge_pos.x, data.badge_pos.y, data.badge)]

    def _final_flag(self, badge_pos, badge_type):
        """Drapeau planté sur la plateforme située sous la position du badge."""
        x = badge_pos.x + BADGE_SIZE[0] // 2
        below = [p for p in self.platforms if p.rect.left <= x < p.rect.right and p.rect.top > badge_pos.y]
        top = min(below, key=lambda p: p.rect.top).rect.top
        return FinalFlag((x, top), badge_type)

    def next_level(self):
        """Passe au niveau suivant"""
        next_level = f"level_{self.number + 1}"

        if next_level in self.levels:
            self.current_level = next_level
            self.load_level()
            return True
        return False
