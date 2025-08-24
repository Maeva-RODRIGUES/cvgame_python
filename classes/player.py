import pygame as pg
from utils import load_image

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image, self.rect = load_image("player/idle.png", size=(128, 128))
        self.rect.x = x
        self.velocity = pg.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False

    def update(self, keys):
        # Mouvement horizontal
        if keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
        elif keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

        # Saut
        if keys[pg.K_SPACE] and self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False

        # Gravité
        self.velocity.y += self.gravity

        # Mouvements
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Sol temporaire
        if self.rect.bottom >= 700:  
            self.rect.bottom = 700
            self.velocity.y = 0
            self.on_ground = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)
