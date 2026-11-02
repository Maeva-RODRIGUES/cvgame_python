from settings import SCREEN_WIDTH
from utils import load_image


class Ground:
    """Sol infini : une tuile répétée qui défile avec la caméra."""

    def __init__(self, y):
        self.tile, _ = load_image("objects/platform.png")
        self.y = y

    def draw(self, surface, camera_x):
        tile_width = self.tile.get_width()
        # Le modulo fait boucler le motif : on ne dessine que les tuiles visibles
        offset = -(camera_x % tile_width)
        for i in range(SCREEN_WIDTH // tile_width + 2):
            surface.blit(self.tile, (offset + i * tile_width, self.y))
