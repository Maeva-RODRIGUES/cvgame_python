import json
import re

import pytest

from classes.level_data import LevelData, LevelDataError, Position, load_levels


@pytest.fixture
def raw_levels(levels_path):
    """Contenu brut de levels.json, à modifier dans chaque test."""
    return json.loads(levels_path.read_text(encoding="utf-8"))


def write(tmp_path, content):
    path = tmp_path / "levels.json"
    path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
    return path


def test_real_file_is_valid(levels_path):
    levels = load_levels(levels_path)
    assert list(levels) == [f"level_{n}" for n in range(1, 8)]
    assert all(isinstance(level, LevelData) for level in levels.values())
    assert isinstance(levels["level_1"].badge_pos, Position)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda d: d["level_4"].update(badge="abap"), "level_4, champ 'badge' : 'abap' inconnu"),
        (lambda d: d["level_2"].pop("width"), "level_2 : champ(s) manquant(s) : width"),
        (lambda d: d["level_2"].update(couleur="rose"), "level_2 : champ(s) inconnu(s) : couleur"),
        (
            lambda d: d["level_5"]["platforms"][1].update(y="400"),
            "level_5, platforms[1], champ 'y' : nombre entier attendu",
        ),
        (
            lambda d: d["level_1"]["badge_pos"].update(x=True),
            "level_1, badge_pos, champ 'x' : nombre entier attendu",
        ),
        (lambda d: d.update(level_9=d.pop("level_7")), "noms de niveaux attendus"),
        (lambda d: d.clear(), "aucun niveau défini"),
    ],
    ids=["badge inconnu", "champ manquant", "champ inconnu", "texte", "booléen", "trou", "vide"],
)
def test_invalid_data_gives_a_clear_error(tmp_path, raw_levels, mutate, message):
    mutate(raw_levels)
    with pytest.raises(LevelDataError, match=re.escape(message)):
        load_levels(write(tmp_path, raw_levels))


def test_broken_json(tmp_path):
    with pytest.raises(LevelDataError, match="JSON invalide"):
        load_levels(write(tmp_path, '{"level_1": '))
