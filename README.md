# Conveniently cheat at Wordle

## Installation

Clone this repo, install [poetry](https://python-poetry.org) if you haven't already, then run `poetry install`.

## Cheating

Run `cheat_at_wordle`.

Make a guess. When Wordle gives you the results of that guess, update the tool to narrow down the list of possible words:

- `> +abc`: The word has "a", "b", and "c" in it.
- `> -def`: The word doesn't have "d", "e", or "f" in it.
- `> 1=g`: The word's first letter is "a"
- `> 2!h`: The word's second letter is not "h"
- `> g.abc`: The word's first letter is "g". The 3rd-5th are "abc".
- `> \`: Show all remaining possibilities in increasing order of likelihood.

Repeat until you've successfully cheated at a fun little game!

## Credits

`words_alpha.txt` comes from [dwyl/english-words](https://github.com/dwyl/english-words/tree/master).