"""python -m textstats FILE: print the statistics of a text file."""
import sys

from textstats import line_count, mean_word_length, top_words, word_count

# Cc only: escaping every non-printable character would also change ordinary words (ZWNJ, ZWJ).
_CONTROL_ESCAPES = {c: f"\\x{c:02x}" for c in [*range(0x20), *range(0x7F, 0xA0)]}


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python -m textstats FILE", file=sys.stderr)
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        if isinstance(e, OSError) and e.strerror is not None:
            reason = e.strerror
        else:
            reason = str(e)
        # The path is escaped as the top words are: a newline in it would split this line.
        print(f"textstats: {args[0].translate(_CONTROL_ESCAPES)}: {reason}", file=sys.stderr)
        return 1
    print(f"words: {word_count(text)}")
    print(f"lines: {line_count(text)}")
    print(f"mean word length: {mean_word_length(text):.2f}")
    top = ", ".join(
        f"{word.translate(_CONTROL_ESCAPES)} ({count})" for word, count in top_words(text, 3)
    )
    print(f"top words: {top}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
