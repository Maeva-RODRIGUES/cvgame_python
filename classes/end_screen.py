import json

import pygame
from settings import SCREEN_WIDTH, BADGE_TYPES, TEXT_COLOR, GOLD, NEON_BLUE
from utils import wrap_text

SKILL_ICON_SIZE = 48
SKILL_STEP = 160
LINE_HEIGHT = 26
LEFT_X, LEFT_WIDTH = 80, 540
RIGHT_X, RIGHT_WIDTH = 680, 540


class EndScreen:
    """Écran de fin : compétences ramassées, réalisations, formations, contact."""

    def __init__(self, content_path, badge_sprites):
        with open(content_path, "r", encoding="utf-8") as f:
            self.content = json.load(f)
        self.icons = {
            badge_type: pygame.transform.scale(sprite, (SKILL_ICON_SIZE, SKILL_ICON_SIZE))
            for badge_type, sprite in badge_sprites.items()
        }
        self.title_font = pygame.font.Font(None, 44)
        self.heading_font = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen, collected):
        c = self.content
        self._centered(screen, self.title_font.render(c["title"], True, GOLD), 45)

        # Compétences : les badges ramassés, avec leur nom
        self._centered(screen, self.heading_font.render(c["skills_title"], True, NEON_BLUE), 95)
        skills = [t for t in BADGE_TYPES if t in collected]
        x = SCREEN_WIDTH // 2 - (len(skills) - 1) * SKILL_STEP // 2
        for badge_type in skills:
            screen.blit(self.icons[badge_type], self.icons[badge_type].get_rect(center=(x, 145)))
            label = self.font.render(c["skills"][badge_type], True, TEXT_COLOR)
            screen.blit(label, label.get_rect(center=(x, 185)))
            x += SKILL_STEP

        # Colonne gauche : réalisations
        self._section(screen, c["achievements_title"], c["achievements"], LEFT_X, 235, LEFT_WIDTH)

        # Colonne droite : formations, contact, disponibilité
        y = self._section(screen, c["education_title"], c["education"], RIGHT_X, 235, RIGHT_WIDTH)
        y = self._section(screen, c["contact_title"], c["contact"], RIGHT_X, y + 16, RIGHT_WIDTH, bullets=False)
        screen.blit(self.heading_font.render(c["availability"], True, GOLD), (RIGHT_X, y + 16))

        # Commandes, qui clignotent
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self._centered(screen, self.font.render(c["controls"], True, GOLD), 680)

    def _section(self, screen, title, items, x, y, width, bullets=True):
        """Titre + liste (puces et retour à la ligne aligné). Renvoie le y sous la section."""
        screen.blit(self.heading_font.render(title, True, NEON_BLUE), (x, y))
        y += 40
        indent = self.font.size("•  ")[0] if bullets else 0
        for item in items:
            if bullets:
                screen.blit(self.font.render("•", True, GOLD), (x, y))
            for line in wrap_text(item, self.font, width - indent):
                screen.blit(self.font.render(line, True, TEXT_COLOR), (x + indent, y))
                y += LINE_HEIGHT
            y += 8
        return y

    @staticmethod
    def _centered(screen, surface, y):
        screen.blit(surface, surface.get_rect(center=(SCREEN_WIDTH // 2, y)))
