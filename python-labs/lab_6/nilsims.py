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
        # po prostu teksty długości 3
        return [text[i:i + 3] for i in range(len(text) - 2)]

    def _rolling_hash(self, text: str) -> list[int]:
        """
        Oblicza rolling hash dla tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista wartości rolling hash
        """
        base = 257  # więcej niż 256
        mod = 10 ** 9 + 7
        n = len(text)
        hashes = []

        if n == 0:
            return hashes

        # hash dla pierwszego znaku
        h1 = ord(text[0]) % mod
        hashes.append(h1)

        if n == 1:
            return hashes

        # hash dla 2 znaku
        h2 = (h1 * base + ord(text[1])) % mod
        hashes.append(h2)

        if n < 3:
            return hashes

        # ta stała jest nie zmienna (base ** <długość trigramu - 1>) % mod
        big = (base ** 2) % mod

        # Hash dla pierwszego trigramu
        rolling = (h2 * base + ord(text[2])) % mod
        hashes.append(rolling)

        # główna pętla dla rolling hashu
        for i in range(3, n):
            left_char_val = (ord(text[i - 3]) * big) % mod  # wartość znaku 2 w lewo
            rolling = (rolling - left_char_val + mod) % mod  # usuwamy tą wartość
            rolling = (rolling * base) % mod  # przesuwamy okno w lewo
            rolling = (rolling + ord(text[i])) % mod  # dodajemy nowy element
            hashes.append(rolling)  # dodajemy nowy hash

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
        hashes = self._rolling_hash(text)

        # Mapujemy rolling hashe na zakres 0–255 i zliczamy częstotliwości
        for h in hashes:
            index = h % self.hash_size
            freq[index] += 1

        avg = sum(freq) / self.hash_size  # średnia częstotliwość
        bits = [f > avg for f in freq]  # tablica booli czy większe niż avg

        # Konwersja do 256-bitowego wyniku
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
        matching_bits = sum(  # zliczamy liczbę takich samych bitów
            8 - bin(b1 ^ b2).count('1')
            for b1, b2 in zip(hash1, hash2)
        )
        # stosunek pasujących bitów do wszystkich bitów => przedział [0, 1]
        return matching_bits / self.hash_size


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
    # po prostu hash dla obu i sprawdzamy ich compare_hashes
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
    # liczymy hash tekstu w celu prównania z kandydatami
    h_target = nh.compute_hash(target)
    results = []

    # dla każdego kandydata
    for it, candidate in enumerate(candidates):
        # obliczamy hash
        h_cand = nh.compute_hash(candidate)
        # sprawdzamy jak bardzo jest podobne
        similarity = nh.compare_hashes(h_target, h_cand)
        if similarity >= threshold:
            # jak podobieństwo większe niż wymagane dodajemy do wyniku
            results.append((it, similarity))

    return results
