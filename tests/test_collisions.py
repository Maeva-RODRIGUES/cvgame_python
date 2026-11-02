import pygame

from classes.game import Game, State
from classes.platform import Platform
from classes.player import Player
from settings import GROUND_Y
from tests.conftest import FakeKeys

NO_KEYS = FakeKeys()


def run(player, frames, platforms, keys=NO_KEYS):
    for _ in range(frames):
        player.update(keys, GROUND_Y, platforms)


def test_falling_player_lands_on_platform():
    platform = Platform(100, 400, 200)
    player = Player(0, 0)
    player.place(150, 300)  # au-dessus de la plateforme, en l'air
    run(player, 60, [platform])
    assert player.on_ground
    assert player.rect.bottom == platform.rect.top


def test_platform_can_be_crossed_from_below():
    # Plateforme à 100 px au-dessus du sol : le saut (~141 px) la traverse
    platform = Platform(0, GROUND_Y - 100, 300)
    player = Player(0, 0)
    player.place(100, GROUND_Y)
    player.on_ground = True
    player.update(FakeKeys(pygame.K_UP), GROUND_Y, [platform])
    run(player, 10, [platform])
    assert player.rect.bottom < platform.rect.top  # passé au-dessus sans être bloqué
    run(player, 60, [platform])
    assert player.rect.bottom == platform.rect.top  # et il atterrit dessus en retombant


def test_player_misses_platform_when_not_above_it():
    platform = Platform(500, 400, 100)
    player = Player(0, 0)
    player.place(100, 300)
    run(player, 60, [platform])
    assert player.rect.bottom == GROUND_Y


def test_badge_is_collected_only_once():
    game = Game()
    game.new_game()
    game.state = State.PLAYING
    badge = game.levels.badges[0]
    # Joueur debout sur la plateforme sous le badge : il le touche pendant plusieurs frames
    below = min(
        (p for p in game.levels.platforms if p.rect.left <= badge.rect.centerx < p.rect.right),
        key=lambda p: p.rect.top - badge.rect.bottom if p.rect.top > badge.rect.bottom else 10_000,
    )
    game.player.place(badge.rect.x, below.rect.top)
    for _ in range(60):
        game._update_playing()
    assert badge.collected
    assert game.collected == [badge.badge_type]
    assert game.level_complete
