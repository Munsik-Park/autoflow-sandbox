"""Small text statistics."""
from collections import Counter


def word_count(text: str) -> int:
    """The number of words in `text`."""
    return len(text.split())


def line_count(text: str) -> int:
    """The number of lines in `text`. A final newline does not start another line."""
    return len(text.splitlines())


def mean_word_length(text: str) -> float:
    """The mean length of the whitespace-separated words in `text`, 0.0 when there are none."""
    words = text.split()
    return sum(len(w) for w in words) / len(words) if words else 0.0


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """The `n` most frequent words of `text` as (word, count) tuples, most frequent first."""
    if n <= 0:
        return []
    words = (token.strip(".,!?;:\"'()").lower() for token in text.split())
    counts = Counter(word for word in words if word)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]
