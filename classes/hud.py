import pygame

from classes.badge import Badge
from settings import BADGE_SIZE, BADGE_TYPES, GOLD, NEON_BLUE, SCREEN_WIDTH, TEXT_COLOR

HUD_MARGIN = 16
BADGE_GAP = 6


class Hud:
    """Bandeau d'informations en haut de l'écran pendant la partie."""

    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        # Un sprite par type de badge, réutilisé à chaque frame
        self.sprites = {badge_type: Badge(0, 0, badge_type).sprite for badge_type in BADGE_TYPES}

    def draw(self, screen, level_number, level_count, level_title, collected):
        # À gauche : numéro et titre du niveau
        number = self.font.render(f"Niveau {level_number}/{level_count}", True, GOLD)
        screen.blit(number, (HUD_MARGIN, HUD_MARGIN))
        title = self.font.render(level_title, True, TEXT_COLOR)
        screen.blit(title, (HUD_MARGIN, HUD_MARGIN + number.get_height() + 4))

        # À droite : un emplacement par badge, rempli quand il est ramassé
        step = BADGE_SIZE[0] + BADGE_GAP
        x = SCREEN_WIDTH - HUD_MARGIN - len(BADGE_TYPES) * step + BADGE_GAP
        for badge_type in BADGE_TYPES:
            if badge_type in collected:
                screen.blit(self.sprites[badge_type], (x, HUD_MARGIN))
            else:
                center = (x + BADGE_SIZE[0] // 2, HUD_MARGIN + BADGE_SIZE[1] // 2)
                self._draw_dashed_circle(screen, center, BADGE_SIZE[0] // 2 - 2)
            x += step

    @staticmethod
    def _draw_dashed_circle(screen, center, radius):
        """Cercle en pointillé : emplacement d'un badge pas encore ramassé."""
        rect = pygame.Rect(0, 0, 2 * radius, 2 * radius)
        rect.center = center
        for i in range(0, 12, 2):  # 6 arcs sur 12 segments
            start = i * 3.14159 / 6
            pygame.draw.arc(screen, NEON_BLUE, rect, start, start + 3.14159 / 6, 2)
