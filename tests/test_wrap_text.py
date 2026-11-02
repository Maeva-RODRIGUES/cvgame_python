import pygame
import pytest

from utils import wrap_text

TEXT = (
    "2010-2023 : 13 ans dans les RH. Recruter, accompagner, faire grandir les équipes... "
    "jusqu'à ce que la tech m'attrape !"
)


@pytest.fixture
def font():
    return pygame.font.Font(None, 24)


def test_lines_fit_the_width(font):
    lines = wrap_text(TEXT, font, 200)
    assert len(lines) > 1
    assert all(font.size(line)[0] <= 200 for line in lines)


def test_no_word_lost_or_reordered(font):
    assert " ".join(wrap_text(TEXT, font, 200)).split() == TEXT.split()


def test_short_text_stays_on_one_line(font):
    assert wrap_text("Bonjour", font, 200) == ["Bonjour"]


def test_too_long_word_gets_its_own_line(font):
    long_word = "anticonstitutionnellement" * 3
    assert wrap_text(f"un {long_word} mot", font, 100) == ["un", long_word, "mot"]


def test_empty_text(font):
    assert wrap_text("", font, 200) == []
