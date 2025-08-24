import os
import pygame as pg

# Répertoire des assets
DATA_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name, colorkey=None, scale=None, size=None):
    fullname = os.path.join(DATA_DIR, name)
    try:
        image = pg.image.load(fullname)
    except pg.error as e:
        print(f"Impossible de charger l'image {name} : {e}")
        raise SystemExit(e)

    # Si on fournit une taille exacte → priorité à size
    if size is not None:
        image = pg.transform.scale(image, size)
    else:
        # Sinon, on applique le scale (comme avant)
        if scale is not None:
            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)
            image = pg.transform.scale(image, (width, height))

    # Gestion de la transparence
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        if isinstance(colorkey, (tuple, list)) and len(colorkey) == 3:
            image.set_colorkey(colorkey, pg.RLEACCEL)

    return image, image.get_rect()

