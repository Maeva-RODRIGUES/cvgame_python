"""Configuration commune : Pygame sans fenêtre ni carte son."""

import os

# À définir AVANT d'importer pygame : SDL choisit ses pilotes à l'initialisation
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402
import pytest  # noqa: E402

from settings import LEVELS_PATH  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def pygame_display():
    """Une surface d'affichage factice : convert_alpha() en a besoin pour charger les sprites."""
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


@pytest.fixture
def levels_path():
    return LEVELS_PATH


class FakeKeys:
    """Remplace pygame.key.get_pressed() : `keys[pygame.K_UP]` vaut True si la touche est listée."""

    def __init__(self, *pressed):
        self.pressed = set(pressed)

    def __getitem__(self, key):
        return key in self.pressed
