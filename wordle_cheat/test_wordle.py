"""Wordle tests."""

import pytest
from wordle_cheat import wordle


@pytest.fixture
def search():
    return wordle.Word(wordle.wordlist())


def test_word_count(search):
    assert len(search.candidates) > 9_000


def test_remove_letters(search):
    search -= "ab"
    assert not any("a" in word or "b" in word for word in search.candidates)


def test_require_letter(search):
    search += "ab"
    assert all("a" in word and "b" in word for word in search.candidates)


def test_letter_at_position(search):
    search[1] = "a"
    assert all(word[0] == "a" for word in search.candidates)

    with pytest.raises(TypeError):
        search["a"] = "a"

    with pytest.raises(ValueError, match=r"^index=0 must be between 1 and 5$"):
        search[0] = "a"

    with pytest.raises(ValueError, match=r"^index=6 must be between 1 and 5$"):
        search[6] = "a"
