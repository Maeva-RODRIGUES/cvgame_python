from classes.badge import Badge, FinalFlag
from classes.level import LevelManager
from settings import FINAL_BADGE


def test_starts_on_first_level(levels_path):
    levels = LevelManager(levels_path)
    assert levels.current_level == "level_1"
    assert levels.number == 1
    assert levels.count == 7
    assert levels.title == levels.levels["level_1"].title


def test_loads_platforms_badge_and_width(levels_path):
    levels = LevelManager(levels_path)
    data = levels.levels["level_1"]
    assert levels.width == data.width
    assert len(levels.platforms) == len(data.platforms)
    assert len(levels.badges) == 1
    assert levels.badges[0].badge_type == data.badge


def test_next_level_until_the_end(levels_path):
    levels = LevelManager(levels_path)
    for expected in range(2, levels.count + 1):
        assert levels.next_level() is True
        assert levels.number == expected
    # Plus de niveau : fin de partie, on reste sur le dernier
    assert levels.next_level() is False
    assert levels.number == levels.count


def test_last_level_has_the_final_flag(levels_path):
    levels = LevelManager(levels_path)
    for _ in range(levels.count - 1):
        assert type(levels.badges[0]) is Badge  # niveaux 1 à 6 : badge classique
        levels.next_level()
    flag = levels.badges[0]
    assert isinstance(flag, FinalFlag)
    assert flag.badge_type == FINAL_BADGE
    # Le pied du mât est posé sur une plateforme
    assert any(flag.rect.bottom == p.rect.top for p in levels.platforms)
