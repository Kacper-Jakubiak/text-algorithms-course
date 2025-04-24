from collections import deque
from typing import List, Tuple, Optional

class AhoCorasickNode:
    def __init__(self):
        # TODO: Zainicjalizuj struktury potrzebne dla węzła w drzewie Aho-Corasick
        self.goto: dict[str, 'AhoCorasickNode'] = {}
        self.fail: Optional['AhoCorasickNode'] = None
        self.output = []

    def AddIfNew(self, c: str):
        if c not in self.goto:
            self.goto[c] = AhoCorasickNode()
        return self.goto[c]

    def SetFail(self, node: 'AhoCorasickNode'):
        self.fail = node

class AhoCorasick:
    def __init__(self, patterns: List[str]):
        # TODO: Zainicjalizuj strukturę Aho-Corasick i usuń puste wzorce
        self.root = AhoCorasickNode()
        self.patterns = [p for p in patterns if p]  # usuń puste wzorce
        self._build_trie()
        self._build_failure_links()

    def _build_trie(self):
        """Builds the trie structure for the given patterns."""
        # TODO: Zaimplementuj budowanie drzewa typu trie dla podanych wzorców
        for pattern in self.patterns:
            node = self.root
            for char in pattern:
                node.AddIfNew(char)
                node = node.goto[char]
            node.output.append(pattern)
        return

    def _build_failure_links(self):
        """Builds failure links and propagates outputs through them."""
        # TODO: Zaimplementuj tworzenie failure links
        # TODO: Utwórz kolejkę do przechodzenia przez drzewo w szerokość (BFS)
        # TODO: Zainicjalizuj łącza awaryjne dla węzłów na głębokości 1
        # TODO: Użyj BFS do ustawienia łączy awaryjnych dla głębszych węzłów
        # TODO: Propaguj wyjścia przez łącza awaryjne
        queue: deque[AhoCorasickNode] = deque()
        for node in self.root.goto.values():
            node.fail = self.root
            queue.append(node)

        while queue:
            u = queue.popleft()
            for c, v in u.goto.items():
                w = u.fail
                while w != self.root and c not in w.goto:
                    w = w.fail
                if c in w.goto:
                    v.fail = w.goto[c]
                else:
                    v.fail = self.root
                v.output += v.fail.output
                queue.append(v)

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches for all occurrences of patterns in the given text.

        Returns:
            List of tuples (start_index, pattern).
        """
        # TODO: Zaimplementuj wyszukiwanie wzorców w tekście
        # TODO: Zwróć listę krotek (indeks_początkowy, wzorzec)
        result = []
        node = self.root
        for i, c in enumerate(text):
            while node != self.root and c not in node.goto:
                node = node.fail

            if c in node.goto:
                node = node.goto[c]
            else:
                node = self.root

            for pattern in node.output:
                result.append((i - len(pattern) + 1, pattern))
        return result

def find_pattern_in_column(text_column: str, pattern_columns: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wszystkie kolumny wzorca w kolumnie tekstu.

    Args:
        text_column: Kolumna tekstu
        pattern_columns: Lista kolumn wzorca

    Returns:
        Lista krotek (pozycja, indeks kolumny), gdzie znaleziono kolumnę wzorca
    """
    # TODO: Zaimplementuj wyszukiwanie kolumn wzorca w kolumnie tekstu
    # TODO: Dla każdej kolumny wzorca, przeszukaj kolumnę tekstu
    # TODO: Zwróć listę krotek (pozycja, indeks kolumny) dla znalezionych dopasowań
    mapped = {pattern: i for i, pattern in enumerate(pattern_columns)}
    ac = AhoCorasick(pattern_columns)
    aho_result = ac.search(text_column)
    result = [(index, mapped[pattern]) for index, pattern in aho_result]
    return result


def find_pattern_2d(text: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wzorzec dwuwymiarowy w tekście dwuwymiarowym.

    Args:
        text: Tekst dwuwymiarowy (lista ciągów znaków tej samej długości)
        pattern: Wzorzec dwuwymiarowy (lista ciągów znaków tej samej długości)

    Returns:
        Lista krotek (i, j), gdzie (i, j) to współrzędne lewego górnego rogu wzorca w tekście
    """
    # TODO: Zaimplementuj wyszukiwanie wzorca dwuwymiarowego
    # TODO: Obsłuż przypadki brzegowe (pusty tekst/wzorzec, wymiary)
    # TODO: Sprawdź, czy wszystkie wiersze mają taką samą długość
    # TODO: Zaimplementuj algorytm wyszukiwania dwuwymiarowego
    # TODO: Zwróć listę współrzędnych lewego górnego rogu dopasowanego wzorca
    if len(text) == 0 or len(pattern) == 0:
        return []
    if all(len(s) == len(text[0]) for s in text) is False or all(len(s) == len(pattern[0]) for s in pattern) is False:
        return []
    if len(text) < len(pattern) or len(text[0]) < len(pattern[0]):
        return []
    T = [[-1] * len(text[0]) for _ in text]
    findings = [find_pattern_in_column(column, pattern) for column in text]
    for i, line in enumerate(findings):
        for j, k in line:
            T[i][j] = k

    result = []
    aho_pattern = ''.join(str(i) for i in range(len(pattern)))
    for j in range(len(text[0])):
        aho_text = ''.join(str(T[i][j]) for i in range(len(text)))
        ac = AhoCorasick([aho_pattern])
        answers = ac.search(aho_text)
        for ans, _ in answers:
            result.append((ans, j))

    return result


if __name__ == '__main__':
    text = [
        "abcabc",
        "defdef",
        "abcabc"
    ]
    pattern = [
        "abc",
        "def"
    ]
    r = find_pattern_2d(text, pattern)
    print(r)