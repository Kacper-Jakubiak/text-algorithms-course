import pytest



class TestUkkonen:
    def test_basic(self):
        pattern = "na"
        text = "ananas"
        tree = SuffixTree(text)
        result = tree.find_pattern(pattern)
        result.sort()
        expected = [1, 3]
        assert result == expected