#!/usr/bin/env python
import re
from collections import Counter
from functools import partial

from wordle_cheat.wordle import Word, wordlist

RE_PLUS = re.compile(r"\+([a-z]+)")
RE_MINUS = re.compile(r"-([a-z]+)")
RE_SET = re.compile(r"([1-5])=([a-z])")
RE_JECT = re.compile(r"([1-5])!([a-z]+)")
RE_MULTI = re.compile(r"([a-z.]{5})")


def letter_counts(words: list[str]) -> dict[str, int]:
    """Count the most common letters in all the words."""
    count: Counter = Counter()  # ಠ_ಠ
    for word in words:
        count.update(word)
    return dict(count)


def word_score(word: str, counts: dict[str, int]):
    """Return the value of the current word, for sorting purposes.

    Words with less common letters are less likely to be in a (purely random) Wordle answer, so
    rate the lower. Words that repeat letters aren't helpful Wordle guesses because they eliminate
    fewer candidates.
    """
    value = sum(counts[letter] for letter in word)

    return value / Counter(word).most_common(1)[0][1]


def main():
    """Play a game of Wordle."""

    words = wordlist()
    sort_key = partial(word_score, counts=letter_counts(words))

    word = Word(words)

    while True:
        print(f"Candidates: {len(word.candidates)}")

        try:
            line = input("> ")
        except EOFError:
            break

        line = line.strip().replace(" ", "")
        if not line:
            continue

        if match := RE_PLUS.fullmatch(line):
            word += match.group(1)
            print()
            continue

        if match := RE_MINUS.fullmatch(line):
            word -= match.group(1)
            print()
            continue

        if match := RE_SET.fullmatch(line):
            index, letter = match.group(1, 2)
            word[int(index)] = letter
            print()
            continue

        if match := RE_JECT.fullmatch(line):
            index, letters = match.group(1, 2)
            word[int(index)] != letters
            print()
            continue

        if match := RE_MULTI.fullmatch(line):
            letters = match.group(1)
            for index, letter in enumerate(letters, 1):
                if letter != ".":
                    word[index] = letter
            print()
            continue

        if line == "/":
            print(sorted(word.candidates, key=sort_key))
            print()
            continue

        print(
            """\
>> What was that?

Type:

> +abc  # The word has "a", "b", and "c" in it.
> -def  # The word doesn't have "d", "e", or "f" in it.
> 1=g   # The word's first letter is "a"
> 2!h   # The word's second letter is not "h"
> g.abc # The word's first letter is "g". The 3rd-5th are "abc".
> \     # Show all remaining possibilities in increasing order of likelihood.
"""
        )


if __name__ == "__main__":
    main()
