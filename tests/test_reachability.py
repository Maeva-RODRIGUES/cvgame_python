"""Atterrissage garanti : chaque plateforme de chaque niveau est atteignable.

On simule de vrais sauts avec la physique du joueur (Player.update) au lieu de
recalculer des formules : si la vitesse, la gravité ou une plateforme change,
le test le voit. Parcours en largeur : depuis le sol, on essaie des sauts
depuis plusieurs points de chaque surface atteinte, dans les deux directions.
"""

import pygame
import pytest

from classes.level import LevelManager
from classes.level_data import load_levels
from classes.player import Player
from settings import GROUND_Y, LEVELS_PATH
from tests.conftest import FakeKeys

# Lecture du JSON seul : à la collecte des tests, Pygame n'est pas encore initialisé
LEVEL_COUNT = len(load_levels(LEVELS_PATH))
GROUND = "sol"


def load(number):
    levels = LevelManager(LEVELS_PATH)
    for _ in range(number - 1):
        levels.next_level()
    return levels


def surface_under(player, levels):
    """Surface sur laquelle le joueur est posé : GROUND, index de plateforme, ou None."""
    if not player.on_ground:
        return None
    if player.rect.bottom == GROUND_Y:
        return GROUND
    for i, platform in enumerate(levels.platforms):
        overlaps_x = (
            player.rect.right > platform.rect.left and player.rect.left < platform.rect.right
        )
        if overlaps_x and player.rect.bottom == platform.rect.top:
            return i
    return None


def jump(player, levels, x, bottom, direction, delay):
    """Saute depuis (x, bottom) ; la direction est tenue à partir de `delay` frames."""
    player.place(x, bottom)
    player.on_ground = True
    for frame in range(200):
        keys = {pygame.K_UP} if frame == 0 else set()
        if direction is not None and frame >= delay:
            keys.add(direction)
        player.update(FakeKeys(*keys), GROUND_Y, levels.platforms, levels.width)
        if frame > 0 and player.on_ground:
            return surface_under(player, levels)
    return None


def reachable_surfaces(levels):
    surfaces = {GROUND: (0, levels.width, GROUND_Y)}
    for i, platform in enumerate(levels.platforms):
        surfaces[i] = (platform.rect.left, platform.rect.right, platform.rect.top)

    player = Player(0, 0)  # un seul joueur réutilisé : charger son image à chaque saut est lent
    reached, todo = {GROUND}, [GROUND]
    while todo:
        left, right, top = surfaces[todo.pop()]
        for x in range(max(0, left - 60), min(right, levels.width - 64), 10):
            for direction in (pygame.K_RIGHT, pygame.K_LEFT, None):
                for delay in (0, 8, 16):
                    landed = jump(player, levels, x, top, direction, delay)
                    if landed is not None and landed not in reached:
                        reached.add(landed)
                        todo.append(landed)
    return reached


@pytest.mark.parametrize("number", range(1, LEVEL_COUNT + 1))
def test_every_platform_is_reachable(number):
    levels = load(number)
    reached = reachable_surfaces(levels)
    missing = [i for i in range(len(levels.platforms)) if i not in reached]
    assert not missing, f"niveau {number} : plateformes inaccessibles {missing}"


@pytest.mark.parametrize("number", range(1, LEVEL_COUNT + 1))
def test_badge_can_be_touched(number):
    """Le badge est touché en sautant depuis une plateforme (pas forcément en restant dessus)."""
    levels = load(number)
    badge = levels.badges[0].rect.inflate(0, 12)  # le badge flotte de quelques pixels
    player = Player(0, 0)
    for platform in levels.platforms:
        for x in range(platform.rect.left - 60, platform.rect.right, 10):
            player.place(x, platform.rect.top)
            player.on_ground = True
            for frame in range(80):
                keys = FakeKeys(pygame.K_UP) if frame == 0 else FakeKeys()
                if player.rect.colliderect(badge):
                    return
                player.update(keys, GROUND_Y, levels.platforms, levels.width)
    pytest.fail(f"niveau {number} : badge impossible à toucher")
