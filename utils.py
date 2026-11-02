import pygame as pg

from settings import ASSETS_DIR


def load_image(name, colorkey=None, scale=None, size=None):
    """Charge assets/<name>. colorkey=-1 : la couleur du pixel (0, 0) devient transparente."""
    fullname = ASSETS_DIR / name
    try:
        image = pg.image.load(fullname)
    except pg.error as e:
        print(f"Impossible de charger l'image {name} : {e}")
        raise SystemExit(e) from e

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
            colorkey = image.get_at((0, 0))  # Color RGBA (4 valeurs), acceptée par set_colorkey
        image.set_colorkey(colorkey, pg.RLEACCEL)

    return image, image.get_rect()


def wrap_text(text, font, max_width):
    """Découpe le texte en lignes dont la largeur en pixels ne dépasse pas `max_width`."""
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}" if current else word
        if current and font.size(candidate)[0] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines
