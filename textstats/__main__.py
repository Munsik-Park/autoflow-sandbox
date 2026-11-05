"""python -m textstats FILE: print the statistics of a text file."""
import sys

from textstats import line_count, mean_word_length, top_words, word_count


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python -m textstats FILE", file=sys.stderr)
        return 2
    with open(args[0], encoding="utf-8") as f:
        text = f.read()
    print(f"words: {word_count(text)}")
    print(f"lines: {line_count(text)}")
    print(f"mean word length: {mean_word_length(text):.2f}")
    top = ", ".join(f"{word} ({count})" for word, count in top_words(text, 3))
    print(f"top words: {top}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
