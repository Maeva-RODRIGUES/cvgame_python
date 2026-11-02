import pygame as pg
from settings import PLAYER_SPEED, PLAYER_SIZE, PLAYER_JUMP_STRENGTH, GRAVITY
from utils import load_image


class Player(pg.sprite.Sprite):
    """Joueur. `rect` est une position dans le MONDE, pas à l'écran."""

    def __init__(self, x, y):
        super().__init__()
        self.image, self.rect = load_image("player/idle.png", size=PLAYER_SIZE)
        self.rect.x = x
        self.rect.y = y
        # Position verticale exacte : un Rect ne stocke que des entiers,
        # les arrondis fausseraient la hauteur du saut
        self.y = float(self.rect.y)
        self.velocity = pg.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.jump_strength = -PLAYER_JUMP_STRENGTH
        self.on_ground = False

    def place(self, x, bottom):
        """Place le joueur (pieds en `bottom`) et remet sa vitesse à zéro."""
        self.rect.x = x
        self.rect.bottom = bottom
        self.y = float(self.rect.y)
        self.velocity.update(0, 0)

    def update(self, keys, ground_y, platforms=(), level_width=None):
        # Mouvement horizontal
        if keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
        elif keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

        # Saut (flèche du haut ; Espace est réservé à la bulle)
        if keys[pg.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength

        # Gravité
        self.velocity.y += self.gravity

        # Déplacement horizontal, borné aux limites du niveau
        self.rect.x += self.velocity.x
        if self.rect.left < 0:
            self.rect.left = 0
        if level_width is not None and self.rect.right > level_width:
            self.rect.right = level_width

        # Déplacement vertical
        old_bottom = self.rect.bottom
        self.y += self.velocity.y
        self.rect.y = round(self.y)
        self.on_ground = False

        # Plateformes traversables : on n'atterrit qu'en tombant,
        # si les pieds étaient au-dessus du dessus de la plateforme
        if self.velocity.y >= 0:
            for platform in platforms:
                top = platform.rect.top
                overlaps_x = (
                    self.rect.right > platform.rect.left
                    and self.rect.left < platform.rect.right
                )
                if overlaps_x and old_bottom <= top <= self.rect.bottom:
                    self._land(top)
                    break

        # Sol
        if self.rect.bottom >= ground_y:
            self._land(ground_y)

    def _land(self, top):
        self.rect.bottom = top
        self.y = float(self.rect.y)
        self.velocity.y = 0
        self.on_ground = True

    def draw(self, surface, camera_x):
        # Conversion monde -> écran au moment du dessin
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
