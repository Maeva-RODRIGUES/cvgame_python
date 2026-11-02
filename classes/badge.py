import math
import random

import pygame

from settings import (
    ASSETS_DIR,
    BADGE_SIZE,
    BADGES_PATH,
    BLACK,
    FLAG_HEIGHT,
    GOLD,
    NEON_BLUE,
    NEON_PINK,
    WHITE,
)
from utils import load_image

# Sprite de secours : couleur et lettres par type de badge
FALLBACK_COLORS = {
    "rh": NEON_PINK,
    "reconversion": NEON_BLUE,
    "web": GOLD,
    "backend": (128, 255, 128),  # Vert clair
    "fullstack": (255, 128, 0),  # Orange
    "data": (128, 0, 255),  # Violet
    "objectif": (255, 255, 128),  # Jaune clair
}
FALLBACK_LETTERS = {
    "rh": "RH",
    "reconversion": "R",
    "web": "W",
    "backend": "B",
    "fullstack": "FS",
    "data": "D",
    "objectif": "O",
}


class Badge:
    """Badge à ramasser. `rect` est en coordonnées monde."""

    def __init__(self, x, y, badge_type):
        self.rect = pygame.Rect(x, y, BADGE_SIZE[0], BADGE_SIZE[1])
        self.badge_type = badge_type
        self.collected = False

        # Animation de flottement
        self.float_offset = 0
        self.float_direction = 1
        self.original_y = y

        self.sprite = self.load_sprite()
        self.glow = self.create_glow()

    def load_sprite(self):
        """Charge assets/badges/badge_<type>.png, ou un sprite de secours s'il n'existe pas."""
        filename = BADGES_PATH + f"badge_{self.badge_type}.png"
        if not (ASSETS_DIR / filename).exists():
            return self.create_fallback_sprite()
        image, _ = load_image(filename, size=BADGE_SIZE)
        return image.convert_alpha()

    def create_fallback_sprite(self):
        """Hexagone coloré avec une lettre, sur fond transparent."""
        sprite = pygame.Surface(BADGE_SIZE, pygame.SRCALPHA)

        center = (BADGE_SIZE[0] // 2, BADGE_SIZE[1] // 2)
        radius = min(BADGE_SIZE) // 2 - 2
        points = [
            (
                center[0] + radius * math.cos(i * math.pi / 3),
                center[1] + radius * math.sin(i * math.pi / 3),
            )
            for i in range(6)
        ]
        pygame.draw.polygon(sprite, FALLBACK_COLORS.get(self.badge_type, WHITE), points)
        pygame.draw.polygon(sprite, WHITE, points, 2)

        font = pygame.font.Font(None, 20)
        text = font.render(FALLBACK_LETTERS.get(self.badge_type, "?"), True, BLACK)
        sprite.blit(text, text.get_rect(center=center))
        return sprite

    @staticmethod
    def create_glow():
        """Halo blanc semi-transparent (l'alpha ne marche que sur une surface SRCALPHA)."""
        glow = pygame.Surface((BADGE_SIZE[0] + 10, BADGE_SIZE[1] + 10), pygame.SRCALPHA)
        glow.fill((255, 255, 255, 50))
        return glow

    def update(self):
        """Animation de flottement (logique, appelée à chaque frame)."""
        if self.collected:
            return
        self.float_offset += 0.1 * self.float_direction
        if abs(self.float_offset) > 5:
            self.float_direction *= -1
        self.rect.y = self.original_y + int(self.float_offset)

    def collect(self):
        """Marque le badge comme ramassé : il ne sera plus ni touché ni dessiné."""
        self.collected = True

    def draw(self, screen, camera_x):
        if self.collected:
            return
        x = self.rect.x - camera_x
        y = self.rect.y
        screen.blit(self.glow, (x - 5, y - 5))
        screen.blit(self.sprite, (x, y))

        # Particules dorées autour du badge
        cx, cy = x + self.rect.width // 2, y + self.rect.height // 2
        for _ in range(3):
            size = random.randint(1, 3)
            pygame.draw.rect(
                screen,
                GOLD,
                (cx + random.randint(-20, 20), cy + random.randint(-20, 20), size, size),
            )


class FinalFlag(Badge):
    """Drapeau final : remplace le dernier badge, planté sur sa plateforme.

    `midbottom` : point (monde) où le pied du mât touche la plateforme.
    """

    def __init__(self, midbottom, badge_type):
        super().__init__(0, 0, badge_type)
        self.rect = self.sprite.get_rect(midbottom=midbottom)

    def load_sprite(self):
        image, _ = load_image("objects/final_flag.png")
        image = image.convert_alpha()
        # Le fichier a de grandes marges transparentes : on garde la zone visible
        visible = image.subsurface(image.get_bounding_rect(min_alpha=16))
        width = round(visible.get_width() * FLAG_HEIGHT / visible.get_height())
        return pygame.transform.smoothscale(visible, (width, FLAG_HEIGHT))

    def update(self):
        pass  # le drapeau ne flotte pas

    def draw(self, screen, camera_x):
        if not self.collected:
            screen.blit(self.sprite, (self.rect.x - camera_x, self.rect.y))
