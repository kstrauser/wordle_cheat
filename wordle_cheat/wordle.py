#!/usr/bin/env python
"""Cheat at Wordle."""


import importlib.resources
from string import ascii_lowercase
from typing import Optional


def quoted_list(words: list[str]) -> str:
    """Make a comma-joined list of quoted words."""

    return ", ".join(f'"{word}"' for word in words)


def pretty_words(words: list[str]) -> str:
    """Pretty-print a list of words."""

    if len(words) <= 50:
        return quoted_list(words)
    return (
        quoted_list(words[:10])
        + f", ({len(words)-20} others) , "
        + quoted_list(words[-10:])
    )


def goodwords(words: list[str]) -> list[str]:
    """Return a sorted list of all unique, valid Wordle answers from the list."""

    return sorted(
        {
            word.lower()
            for word in words
            if len(word) == 5 and word.isalpha() and word.isascii()
        }
    )


def wordlist() -> list[str]:
    """Return all of the good words from the package's list."""

    word_file = importlib.resources.files("data") / "words_alpha.txt"
    return goodwords(word_file.read_text().splitlines())


class Letter:
    """Represent a single letter in a Search."""

    def __init__(self, word: "Word", index: int, letters: set[str]):
        self.word: Optional["Word"] = word
        self.index = index
        self.letters = letters

    def __ne__(self, letters: str):  # type: ignore[override]
        if not self.word:
            raise TypeError("This Letter is no longer connected to a Word.")
        self.word.remove(self.index, letters)

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        if self.word:
            return base_repr
        return f"Detached {base_repr}"

    def __str__(self) -> str:
        count = len(self.letters)
        if count == 26:
            return ascii_lowercase
        if count == 1:
            return list(self.letters)[0].upper()
        if count == 2:
            return "[" + "".join(sorted(self.letters)) + "]"
        if count < 6:
            return ",".join(sorted(self.letters))
        return "".join(
            letter if letter in self.letters else "." for letter in ascii_lowercase
        )


def validate_index(index: int):
    if not isinstance(index, int):
        raise TypeError(f"{index=} must be an int.")

    if not 1 <= index <= 5:
        raise ValueError(f"{index=} must be between 1 and 5")


class Word:
    """Represent a word from a Wordle challenge."""

    def __init__(self, candidates: list[str]):
        """Create a word searcher."""
        self.letters: dict[int, Letter] = {}
        self.candidates = goodwords(candidates)

    @property
    def candidates(self) -> list[str]:
        return self._candidates

    @candidates.setter
    def candidates(self, candidates: list[str]):
        self._candidates = candidates
        for letter in self.letters.values():
            letter.word = None
        self.letters = {
            index + 1: Letter(self, index + 1, {word[index] for word in candidates})
            for index in range(5)
        }

    def remove(self, index: int, letters: str):
        validate_index(index)
        letters = letters.lower()
        self.candidates = [
            word for word in self.candidates if word[index - 1] not in letters
        ]

    def __getitem__(self, index: int) -> Letter:
        validate_index(index)
        return self.letters[index]

    def __setitem__(self, index, letter: str):
        """Discard words that don't contain the given letter at that index."""
        validate_index(index)
        letter = letter.lower()
        if len(letter) != 1:
            raise ValueError("__setitem__ accepts exactly one letter.")
        self.candidates = [
            word for word in self.candidates if word[index - 1] == letter
        ]

    def __iadd__(self, letters: str) -> "Word":
        """Remove all words without the given letters from this Search."""
        letters = letters.lower()
        self.candidates = [
            word
            for word in self.candidates
            if all(letter in word for letter in letters)
        ]
        return self

    def __isub__(self, letters: str) -> "Word":
        """Remove words with the given letters from this Search."""
        letters = letters.lower()
        self.candidates = [
            word
            for word in self.candidates
            if not any(letter in word for letter in letters)
        ]
        return self

    def __repr__(self):
        lines = [pretty_words(self.candidates)]
        lines.append(f"{len(self.candidates)} total")
        for i in range(1, 6):
            lines.append(f"  {i}: {self.letters[i]}")
        return "\n".join(lines)
