# autoflow-sandbox

A small repository for trying [autoflow-coordinator](https://github.com/Munsik-Park/autoflow-coordinator) and [autoflow-ide](https://github.com/Munsik-Park/Autoflow-ide) on short runs.

`textstats` counts the words, lines and mean word length of a text, and lists its most frequent words with `top_words(text, n)`.

```
python -m textstats FILE
```

## Development

Python 3.9 or later, standard library only.

```
python -m unittest -v
```

## Issues

The open issues are graded by size with a label, so a run can be picked by how long it should take:

| Label | Change | Suggested reference workflow |
|---|---|---|
| `size:tiny` | A document fix | review-only |
| `size:small` | A bug with a known cause | analysis-review |
| `size:medium` | A small feature | full |

The tag `seed` marks the state the issues were written against.

## License

[Apache License 2.0](LICENSE)
