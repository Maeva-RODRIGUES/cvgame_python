"""Chargement et validation de data/levels.json.

Chaque niveau est converti en dataclasses typées. Si le fichier est mal formé
(champ manquant, mauvais type, badge inconnu...), une LevelDataError indique
le niveau et le champ concernés au lieu d'un plantage plus loin dans le jeu.
"""
import json
from dataclasses import dataclass

from settings import BADGE_TYPES


class LevelDataError(ValueError):
    """Erreur de contenu dans le fichier des niveaux."""


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class PlatformData:
    x: int
    y: int
    width: int


@dataclass(frozen=True)
class LevelData:
    title: str
    dialogue: str
    badge: str
    width: int
    platforms: list[PlatformData]
    badge_pos: Position


def load_levels(path):
    """Lit le JSON et renvoie {"level_1": LevelData, ...}, ou lève LevelDataError."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        raise LevelDataError(f"JSON invalide ({e})") from e

    _check_type(raw, dict, "fichier")
    if not raw:
        raise LevelDataError("aucun niveau défini")

    # Les niveaux s'enchaînent par numéro (level_1, level_2...) : pas de trou permis
    expected = [f"level_{n}" for n in range(1, len(raw) + 1)]
    if sorted(raw, key=_level_number) != expected:
        raise LevelDataError(f"noms de niveaux attendus : {', '.join(expected)} (trouvés : {', '.join(raw)})")

    return {name: _parse_level(data, name) for name, data in raw.items()}


def _level_number(name):
    _, _, number = name.partition("_")
    return int(number) if number.isdigit() else 0


def _parse_level(data, where):
    _check_type(data, dict, where)
    _check_fields(data, ["title", "dialogue", "badge", "width", "platforms", "badge_pos"], where)

    badge = _get(data, "badge", str, where)
    if badge not in BADGE_TYPES:
        raise LevelDataError(
            f"{where}, champ 'badge' : '{badge}' inconnu (attendu : {', '.join(BADGE_TYPES)})"
        )

    platforms = _get(data, "platforms", list, where)
    return LevelData(
        title=_get(data, "title", str, where),
        dialogue=_get(data, "dialogue", str, where),
        badge=badge,
        width=_get(data, "width", int, where),
        platforms=[_parse_platform(p, f"{where}, platforms[{i}]") for i, p in enumerate(platforms)],
        badge_pos=_parse_position(_get(data, "badge_pos", dict, where), f"{where}, badge_pos"),
    )


def _parse_platform(data, where):
    _check_type(data, dict, where)
    _check_fields(data, ["x", "y", "width"], where)
    return PlatformData(*(_get(data, name, int, where) for name in ("x", "y", "width")))


def _parse_position(data, where):
    _check_fields(data, ["x", "y"], where)
    return Position(_get(data, "x", int, where), _get(data, "y", int, where))


def _check_fields(data, names, where):
    """Champs obligatoires présents, et aucun champ inconnu (faute de frappe)."""
    missing = [n for n in names if n not in data]
    if missing:
        raise LevelDataError(f"{where} : champ(s) manquant(s) : {', '.join(missing)}")
    unknown = [n for n in data if n not in names]
    if unknown:
        raise LevelDataError(f"{where} : champ(s) inconnu(s) : {', '.join(unknown)}")


def _get(data, name, expected_type, where):
    value = data[name]
    _check_type(value, expected_type, f"{where}, champ '{name}'")
    return value


TYPE_NAMES = {str: "texte", int: "nombre entier", list: "liste", dict: "objet"}


def _check_type(value, expected_type, where):
    # bool est une sous-classe de int en Python : true/false ne doivent pas passer pour des nombres
    if not isinstance(value, expected_type) or (expected_type is int and isinstance(value, bool)):
        raise LevelDataError(
            f"{where} : {TYPE_NAMES[expected_type]} attendu, reçu {value!r}"
        )
