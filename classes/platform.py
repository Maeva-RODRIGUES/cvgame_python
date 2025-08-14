import pygame as pg
from settings import SCREEN_WIDTH
from utils import load_image

class Platform(pg.sprite.Sprite):
    def __init__(self, y_pos):
        super().__init__()

        # Charge la tuile du sol
        tile_image, tile_rect = load_image("objects/platform.png", scale=1)

        # Crée une surface de la largeur de l'écran
        self.image = pg.Surface((SCREEN_WIDTH, tile_rect.height), pg.SRCALPHA)

        # Répète la tuile horizontalement
        for x in range(0, SCREEN_WIDTH, tile_rect.width):
            self.image.blit(tile_image, (x, 0))

        # Position du sol sur l'écran
        self.rect = self.image.get_rect(topleft=(0, y_pos))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
  