import unittest

from textstats import line_count, mean_word_length, word_count


class WordCount(unittest.TestCase):
    def test_single_spaces(self):
        self.assertEqual(word_count("one two three"), 3)


class LineCount(unittest.TestCase):
    def test_lines(self):
        self.assertEqual(line_count("a\nb\nc"), 3)

    def test_final_newline(self):
        self.assertEqual(line_count("a\nb\n"), 2)

    def test_empty(self):
        self.assertEqual(line_count(""), 0)


class MeanWordLength(unittest.TestCase):
    def test_mean(self):
        self.assertAlmostEqual(mean_word_length("ab abcd"), 3.0)

    def test_no_words(self):
        self.assertEqual(mean_word_length("   "), 0.0)


if __name__ == "__main__":
    unittest.main()
