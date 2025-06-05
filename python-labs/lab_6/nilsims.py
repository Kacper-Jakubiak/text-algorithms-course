import hashlib


class NilsimsHash:
    """Klasa implementująca algorytm Nilsimsa."""

    def __init__(self):
        """Inicjalizuje hash Nilsimsa."""
        self.hash_size = 256

    def _trigrams(self, text: str) -> list[str]:
        """
        Generuje trigramy z tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista trigramów
            """
        return [text[i:i + 3] for i in range(len(text) - 2)]

    def _rolling_hash(self, text: str) -> list[int]:
        """
        Oblicza rolling hash dla tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista wartości rolling hash
        """
        hashes = []
        for c in text:
            h = hashlib.sha1(c.encode('utf-8')).digest()
            hashes.append(h[0])
        return hashes

    def compute_hash(self, text: str) -> bytes:
        """
        Oblicza hash Nilsimsa dla tekstu.

        Args:
            text: Tekst do zahashowania

        Returns:
            256-bitowy hash jako bytes
        """
        freq = [0] * self.hash_size
        trigrams = self._trigrams(text)
        for tri in trigrams:
            h = hashlib.sha1(tri.encode('utf-8')).digest()
            for b in h[:3]:
                freq[b] += 1

        avg = sum(freq) / self.hash_size
        bits = [f > avg for f in freq]

        result = bytearray(32)
        for i, bit in enumerate(bits):
            if bit:
                byte_index = i // 8
                bit_index = 7 - (i % 8)
                result[byte_index] |= (1 << bit_index)

        return bytes(result)

    def compare_hashes(self, hash1: bytes, hash2: bytes) -> float:
        """
        Porównuje dwa hashe Nilsimsa i zwraca stopień podobieństwa.

        Args:
            hash1: Pierwszy hash
            hash2: Drugi hash

        Returns:
            Stopień podobieństwa w zakresie [0, 1]
        """
        matching_bits = sum(
            8 - bin(b1 ^ b2).count('1')
            for b1, b2 in zip(hash1, hash2)
        )
        return matching_bits / 256


def nilsims_similarity(text1: str, text2: str) -> float:
    """
    Oblicza podobieństwo między dwoma tekstami używając algorytmu Nilsimsa.

    Args:
        text1: Pierwszy tekst
        text2: Drugi tekst

    Returns:
        Stopień podobieństwa w zakresie [0, 1]
    """
    nh = NilsimsHash()
    h1 = nh.compute_hash(text1)
    h2 = nh.compute_hash(text2)
    return nh.compare_hashes(h1, h2)


def find_similar_texts(target: str, candidates: list[str], threshold: float = 0.7) -> list[tuple[int, float]]:
    """
    Znajduje teksty podobne do tekstu docelowego.

    Args:
        target: Tekst docelowy
        candidates: Lista kandydatów
        threshold: Próg podobieństwa

    Returns:
        Lista krotek (indeks, podobieństwo) dla tekstów powyżej progu
    """
    nh = NilsimsHash()
    h_target = nh.compute_hash(target)
    results = []

    for it, candidate in enumerate(candidates):
        h_cand = nh.compute_hash(candidate)
        similarity = nh.compare_hashes(h_target, h_cand)
        if similarity >= threshold:
            results.append((it, similarity))

    return results
