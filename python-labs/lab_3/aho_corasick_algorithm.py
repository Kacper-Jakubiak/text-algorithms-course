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
        self.patterns = [p for p in patterns if p]
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