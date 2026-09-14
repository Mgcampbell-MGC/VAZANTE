"""Wrap implicitly concatenated string literals in parentheses (ruff ISC004).

The project's ruff config rejects adjacent string literals inside a collection
because they are usually a missing comma. Where they are deliberate, the fix is
a pair of parentheses — which is fiddly to do with a regex and trivial with the
tokenizer, since it hands back exact positions for every STRING token.

    .venv/bin/python scripts/dev/wrap_implicit_concat.py FILE [FILE ...]
"""

from __future__ import annotations

import io
import sys
import token
import tokenize
from pathlib import Path


def wrap(src: str) -> str:
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    runs: list[tuple[tuple[int, int], tuple[int, int]]] = []
    i = 0
    while i < len(toks):
        if toks[i].type != token.STRING:
            i += 1
            continue
        j, last = i + 1, i
        while j < len(toks):
            if toks[j].type == token.STRING:
                last, j = j, j + 1
            elif toks[j].type in (token.NL, token.NEWLINE, token.COMMENT, token.INDENT):
                j += 1
            else:
                break
        # only multi-line runs need wrapping, and only when not already parenthesised
        if last > i and toks[last].end[0] > toks[i].start[0]:
            before = next((t for t in reversed(toks[:i]) if t.type not in
                           (token.NL, token.NEWLINE, token.COMMENT, token.INDENT)), None)
            after = next((t for t in toks[last + 1:] if t.type not in
                          (token.NL, token.NEWLINE, token.COMMENT, token.DEDENT)), None)
            paren = (before is not None and before.string == "("
                     and after is not None and after.string == ")")
            if not paren:
                runs.append((toks[i].start, toks[last].end))
        i = last + 1

    lines = src.split("\n")
    for (sr, sc), (er, ec) in reversed(runs):     # back to front, so offsets hold
        lines[er - 1] = lines[er - 1][:ec] + ")" + lines[er - 1][ec:]
        lines[sr - 1] = lines[sr - 1][:sc] + "(" + lines[sr - 1][sc:]
    return "\n".join(lines)


def main() -> int:
    for p in map(Path, sys.argv[1:]):
        src = p.read_text(encoding="utf-8")
        out = wrap(src)
        if out != src:
            p.write_text(out, encoding="utf-8")
            print(f"wrapped {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
