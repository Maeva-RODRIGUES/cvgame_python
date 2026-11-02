import pygame as pg
from settings import (
    PLATFORM_HEIGHT,
    PLATFORM_COLOR,
    PLATFORM_EDGE_COLOR,
    PLATFORM_EDGE_HEIGHT,
    PLATFORM_TILE_WIDTH,
)


class Platform:
    """Plateforme « traversable » de largeur variable, en coordonnées monde.

    On atterrit dessus en tombant, on la traverse en montant.
    """

    def __init__(self, x, y, width):
        self.rect = pg.Rect(x, y, width, PLATFORM_HEIGHT)
        self.image = self._build_image(width)

    @staticmethod
    def _build_image(width):
        image = pg.Surface((width, PLATFORM_HEIGHT))
        image.fill(PLATFORM_COLOR)
        # Séparations entre blocs, un peu plus sombres
        dark = tuple(c // 2 for c in PLATFORM_COLOR)
        for x in range(PLATFORM_TILE_WIDTH, width, PLATFORM_TILE_WIDTH):
            pg.draw.line(image, dark, (x, 0), (x, PLATFORM_HEIGHT))
        # Liseré néon sur le dessus
        pg.draw.rect(image, PLATFORM_EDGE_COLOR, (0, 0, width, PLATFORM_EDGE_HEIGHT))
        return image

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
