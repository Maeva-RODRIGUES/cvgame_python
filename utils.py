import os
import pygame as pg

# Répertoire
DATA_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name, colorkey=None, scale=1):
    """Charge une image avec mise à l'échelle et transparence facultative."""

    fullname = os.path.join(DATA_DIR, name)
    try:
        image = pg.image.load(fullname)
    except pg.error as e:
        print(f"Impossible de charger l'image {name} : {e}")
        raise SystemExit(e)

    # Mise à l’échelle
    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pg.transform.scale(image, size)

    # Convertir l'image avec alpha (canal de transparence)
    image = image.convert_alpha()

    # Gérer la transparence avec colorkey
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))  # couleur du pixel en haut à gauche
        image.set_colorkey(colorkey, pg.RLEACCEL)

    return image, image.get_rect()
