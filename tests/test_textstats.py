import os
import subprocess
import sys
import tempfile
import unittest

from textstats import line_count, mean_word_length, top_words, word_count


class WordCount(unittest.TestCase):
    def test_single_spaces(self):
        self.assertEqual(word_count("one two three"), 3)

    def test_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_repeated_spaces(self):
        self.assertEqual(word_count("one  two"), 2)

    def test_newline(self):
        self.assertEqual(word_count("one\ntwo"), 2)

    def test_leading_and_trailing_spaces(self):
        self.assertEqual(word_count("  one two  "), 2)

    def test_cli_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sample.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("hello world\nsecond line\n")
            result = subprocess.run(
                [sys.executable, "-m", "textstats", path],
                capture_output=True,
                text=True,
                check=True,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            )
        self.assertIn("words: 4", result.stdout.splitlines())


class LineCount(unittest.TestCase):
    def test_lines(self):
        self.assertEqual(line_count("a\nb\nc"), 3)

    def test_final_newline(self):
        self.assertEqual(line_count("a\nb\n"), 2)

    def test_empty(self):
        self.assertEqual(line_count(""), 0)

    def test_form_feed_does_not_end_a_line(self):
        self.assertEqual(line_count("a\x0cb"), 1)

    def test_vertical_tab_does_not_end_a_line(self):
        self.assertEqual(line_count("a\x0bb"), 1)

    def test_file_separator_does_not_end_a_line(self):
        self.assertEqual(line_count("a\x1cb"), 1)

    def test_next_line_does_not_end_a_line(self):
        self.assertEqual(line_count("a\x85b"), 1)

    def test_line_separator_does_not_end_a_line(self):
        self.assertEqual(line_count("a\N{LINE SEPARATOR}b"), 1)

    def test_group_separator_does_not_end_a_line(self):
        self.assertEqual(line_count("a\x1db"), 1)

    def test_record_separator_does_not_end_a_line(self):
        self.assertEqual(line_count("a\x1eb"), 1)

    def test_paragraph_separator_does_not_end_a_line(self):
        self.assertEqual(line_count("a\N{PARAGRAPH SEPARATOR}b"), 1)

    def test_crlf_ends_a_line(self):
        self.assertEqual(line_count("a\r\nb"), 2)

    def test_cr_ends_a_line(self):
        self.assertEqual(line_count("a\rb"), 2)


class MeanWordLength(unittest.TestCase):
    def test_mean(self):
        self.assertAlmostEqual(mean_word_length("ab abcd"), 3.0)

    def test_no_words(self):
        self.assertEqual(mean_word_length("   "), 0.0)


class TopWords(unittest.TestCase):
    def test_word_is_a_whitespace_run_with_edge_punctuation_removed(self):
        text = (
            "cat. (cat) \"dog\" 'dog' bird, bird!  fish?\tfish;\nant: ant"
            " don't a.b (\"x\"), ... '' ()"
        )
        self.assertCountEqual(
            top_words(text, 100),
            [("cat", 2), ("dog", 2), ("bird", 2), ("fish", 2), ("ant", 2),
             ("don't", 1), ("a.b", 1), ("x", 1)],
        )

    def test_words_are_compared_and_returned_in_lower_case(self):
        self.assertEqual(top_words("Apple APPLE apple", 5), [("apple", 3)])

    def test_equal_counts_are_ordered_alphabetically(self):
        self.assertEqual(top_words("c b a", 2), [("a", 1), ("b", 1)])

    def test_n_zero_or_negative_returns_empty_list(self):
        self.assertEqual(top_words("b a b", 0), [])
        self.assertEqual(top_words("b a b", -1), [])

    def test_n_above_distinct_count_returns_all_words(self):
        self.assertEqual(top_words("b a b", 10), [("b", 2), ("a", 1)])

    def test_example_returns_word_count_tuples_most_frequent_first(self):
        self.assertEqual(
            top_words("The cat. the dog, THE cat!", 2), [("the", 3), ("cat", 2)]
        )


class TopWordsCli(unittest.TestCase):
    def cli_lines(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sample.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            result = subprocess.run(
                [sys.executable, "-m", "textstats", path],
                capture_output=True,
                text=True,
                check=True,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            )
        return result.stdout.splitlines()

    def test_three_most_frequent_words(self):
        self.assertIn(
            "top words: the (3), cat (2), dog (1)",
            self.cli_lines("The cat. the dog, THE cat! fish\n"),
        )

    def test_fewer_than_three_distinct_words(self):
        self.assertIn("top words: hi (2), bye (1)", self.cli_lines("Hi hi (bye)\n"))

    def test_no_words_prints_the_label_and_its_trailing_space_only(self):
        self.assertIn("top words: ", self.cli_lines('... "" ()\n'))

    def test_control_characters_are_escaped_and_printable_words_print_unchanged(self):
        # Every C0 control, DEL and C1 control that can sit inside a word: the others
        # (09-0d, 1c-1f, 85) are whitespace to str.split().
        c0 = [*range(0x00, 0x09), *range(0x0E, 0x1C)]
        c1 = [0x7F, *range(0x80, 0x85), *range(0x86, 0xA0)]
        c0_word = "\x1b[2J\x1b]0;x\x07" + "".join(map(chr, c0))
        persian_with_zwnj = "می‌خواهم"
        c1_word = "\x9b2J" + "".join(map(chr, c1))
        text = " ".join([c0_word] * 3 + [persian_with_zwnj] * 2 + [c1_word]) + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sample.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            result = subprocess.run(
                [sys.executable, "-m", "textstats", path],
                capture_output=True,
                check=True,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            )
        stdout = result.stdout.decode("utf-8")
        c0_printed = "\\x1b[2j\\x1b]0;x\\x07" + "".join("\\x%02x" % c for c in c0)
        c1_printed = "\\x9b2j" + "".join("\\x%02x" % c for c in c1)
        self.assertIn(
            f"top words: {c0_printed} (3), {persian_with_zwnj} (2), {c1_printed} (1)",
            stdout.splitlines(),
        )
        raw = [
            c for c in stdout.replace(os.linesep, "\n")
            if c != "\n" and (c < " " or "\x7f" <= c <= "\x9f")
        ]
        self.assertEqual(raw, [], "raw control characters in stdout")


if __name__ == "__main__":
    unittest.main()
