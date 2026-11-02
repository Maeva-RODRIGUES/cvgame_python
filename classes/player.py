import pygame as pg
from settings import PLAYER_SPEED, PLAYER_SIZE
from utils import load_image


class Player(pg.sprite.Sprite):
    """Joueur. `rect` est une position dans le MONDE, pas à l'écran."""

    def __init__(self, x, y):
        super().__init__()
        self.image, self.rect = load_image("player/idle.png", size=PLAYER_SIZE)
        self.rect.x = x
        self.rect.y = y
        self.velocity = pg.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False

    def update(self, keys, ground_y):
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
            self.on_ground = False

        # Gravité
        self.velocity.y += self.gravity

        # Déplacement dans le monde
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Le joueur ne sort pas par la gauche du monde
        if self.rect.left < 0:
            self.rect.left = 0

        # Atterrissage sur le sol
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity.y = 0
            self.on_ground = True

    def draw(self, surface, camera_x):
        # Conversion monde -> écran au moment du dessin
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
