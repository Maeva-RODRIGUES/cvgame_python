import pygame as pg

from settings import SIGN_HEIGHT
from utils import load_image


class Sign:
    """Panneau de direction posé sur le sol, en coordonnées monde."""

    def __init__(self, x, ground_y):
        image, _ = load_image("objects/direction.png")
        # Le fichier a de grandes marges transparentes : on garde la zone visible
        visible = image.subsurface(image.get_bounding_rect(min_alpha=16))
        width = round(visible.get_width() * SIGN_HEIGHT / visible.get_height())
        self.image = pg.transform.smoothscale(visible.convert_alpha(), (width, SIGN_HEIGHT))
        self.rect = self.image.get_rect(left=x, bottom=ground_y)

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
