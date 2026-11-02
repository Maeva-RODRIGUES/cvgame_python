"""Génère les badges du jeu en pixel art : disque néon 16x16 + icône, agrandi x2 (32x32).

Usage (depuis la racine du projet) :
    python tools/make_badges.py                    # écrit assets/badges/badge_<type>.png
    python tools/make_badges.py --preview out.png  # + planche d'aperçu agrandie
"""
import argparse
from pathlib import Path

import pygame as pg

OUT = Path(__file__).resolve().parent.parent / "assets" / "badges"
SCALE = 2
DARK = (30, 0, 56)

COLORS = {
    "rh": (255, 31, 143),
    "reconversion": (0, 245, 255),
    "web": (255, 217, 61),
    "abap": (128, 255, 128),
    "fullstack": (255, 128, 0),
    "data": (128, 0, 255),
    "objectif": (255, 255, 128),
}

# Icônes 10x10 : "w" = couleur de l'icône, "k" = sombre, "." = rien
ICONS = {
    "rh": [  # une personne : l'humain
        "...wwww...",
        "..wwwwww..",
        "..wwwwww..",
        "...wwww...",
        "..........",
        "..wwwwww..",
        ".wwwwwwww.",
        ".wwwwwwww.",
        ".wwwwwwww.",
        "..........",
    ],
    "reconversion": [  # ampoule : le déclic
        "...wwww...",
        "..wwwwww..",
        ".wwwwwwww.",
        ".wwwwwwww.",
        ".wwwwwwww.",
        "..wwwwww..",
        "...wwww...",
        "...k..k...",
        "...wwww...",
        "....ww....",
    ],
    "web": [  # fenêtre de navigateur
        "wwwwwwwwww",
        "w.w.wwwwww",
        "wwwwwwwwww",
        "w........w",
        "w.wwww...w",
        "w........w",
        "w.wwwwww.w",
        "w........w",
        "wwwwwwwwww",
        "..........",
    ],
    "abap": [  # engrenage : back-end
        "....ww....",
        ".ww.ww.ww.",
        ".wwwwwwww.",
        "..ww..ww..",
        "www....www",
        "www....www",
        "..ww..ww..",
        ".wwwwwwww.",
        ".ww.ww.ww.",
        "....ww....",
    ],
    "fullstack": [  # couches empilées
        "..........",
        "..wwwwww..",
        ".wwwwwwww.",
        "..........",
        "..wwwwww..",
        ".wwwwwwww.",
        "..........",
        "..wwwwww..",
        ".wwwwwwww.",
        "..........",
    ],
    "data": [  # base de données
        "..wwwwww..",
        ".wwwwwwww.",
        ".kwwwwwwk.",
        ".wkkkkkkw.",
        ".wwwwwwww.",
        ".wkkkkkkw.",
        ".wwwwwwww.",
        ".wkkkkkkw.",
        ".wwwwwwww.",
        "..wwwwww..",
    ],
    "objectif": [  # cible
        "...wwww...",
        "..w....w..",
        ".w..ww..w.",
        "w..w..w..w",
        "w.w.ww.w.w",
        "w.w.ww.w.w",
        "w..w..w..w",
        ".w..ww..w.",
        "..w....w..",
        "...wwww...",
    ],
}


def shade(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color)


def make_badge(badge_type):
    base = COLORS[badge_type]
    luminance = 0.299 * base[0] + 0.587 * base[1] + 0.114 * base[2]
    icon_color = (255, 255, 255) if luminance < 150 else DARK  # contraste lisible
    small = pg.Surface((16, 16), pg.SRCALPHA)
    # Disque : contour sombre, reflet clair en haut à gauche
    for y in range(16):
        for x in range(16):
            d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
            if d <= 7.3:
                color = shade(base, 0.45) if d > 6.3 else base
                if d <= 6.3 and x + y < 9:
                    color = tuple(min(255, c + 60) for c in base)
                small.set_at((x, y), (*color, 255))
    for row, line in enumerate(ICONS[badge_type]):
        for col, ch in enumerate(line):
            if ch == "w":
                small.set_at((3 + col, 3 + row), (*icon_color, 255))
            elif ch == "k":
                small.set_at((3 + col, 3 + row), (*shade(base, 0.45), 255))
    return pg.transform.scale(small, (16 * SCALE, 16 * SCALE))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--preview", type=Path, help="chemin de la planche d'aperçu (facultatif)")
    args = parser.parse_args()

    pg.init()
    pg.display.set_mode((1, 1))
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = pg.Surface((7 * 150, 190))
    sheet.fill((43, 14, 63))
    font = pg.font.Font(None, 24)
    for i, badge_type in enumerate(COLORS):
        badge = make_badge(badge_type)
        pg.image.save(badge, OUT / f"badge_{badge_type}.png")
        big = pg.transform.scale(badge, (128, 128))
        sheet.blit(big, (i * 150 + 11, 10))
        sheet.blit(badge, (i * 150 + 59, 145))  # taille réelle en jeu
        label = font.render(badge_type, True, (245, 235, 255))
        sheet.blit(label, label.get_rect(center=(i * 150 + 75, 180)))
    if args.preview:
        pg.image.save(sheet, args.preview)
    print("Badges écrits dans", OUT)


if __name__ == "__main__":
    main()
