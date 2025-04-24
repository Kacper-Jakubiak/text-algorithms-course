def hamming_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Hamminga między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Hamminga (liczba pozycji, na których znaki się różnią)
        Jeśli ciągi mają różne długości, zwraca -1
    """
    # TODO: Zaimplementuj obliczanie odległości Hamminga
    if len(s1) != len(s2):
        return -1
    result = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            result += 1
    return result


def set_nth_bit(n: int) -> int:
    """
    Zwraca maskę bitową z ustawionym n-tym bitem na 1.

    Args:
        n: Pozycja bitu do ustawienia (0-indeksowana)

    Returns:
        Maska bitowa z n-tym bitem ustawionym na 1
    """
    # TODO: Zaimplementuj ustawianie n-tego bitu
    return 1 << n


def nth_bit(m: int, n: int) -> int:
    """
    Zwraca wartość n-tego bitu w masce m.

    Args:
        m: Maska bitowa
        n: Pozycja bitu do odczytania (0-indeksowana)

    Returns:
        Wartość n-tego bitu (0 lub 1)
    """
    # TODO: Zaimplementuj odczytywanie n-tego bitu
    return (m >> n) & 1


def make_mask(pattern: str) -> list:
    """
    Tworzy tablicę masek dla algorytmu Shift-Or.

    Args:
        pattern: Wzorzec do wyszukiwania

    Returns:
        Tablica 256 masek, gdzie każda maska odpowiada jednemu znakowi ASCII
    """
    # TODO: Zaimplementuj tworzenie tablicy masek
    if not pattern:
        return [0xff] * 256
    masks = [0] * 256
    for i, c in enumerate(pattern):
        masks[ord(c)] |= set_nth_bit(i)
    for i in range(256):
        masks[i] = ~masks[i]
    return masks


def fuzzy_shift_or(text: str, pattern: str, k: int = 2) -> list[int]:
    """
    Implementacja przybliżonego wyszukiwania wzorca przy użyciu algorytmu Shift-Or.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania
        k: Maksymalna dopuszczalna liczba różnic (odległość Hamminga)

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
        z maksymalnie k różnicami
    """
    # TODO: Zaimplementuj algorytm przybliżonego wyszukiwania Shift-Or
    # TODO: Obsłuż przypadki brzegowe (pusty wzorzec, wzorzec dłuższy niż tekst, k < 0)
    # TODO: Zaimplementuj główną logikę algorytmu
    n = len(text)
    m = len(pattern)
    if n == 0 or m == 0 or m > n or k < 0:
        return []
    result = []

    masks = make_mask(pattern)
    s = [~0 for _ in range(k + 1)]

    for i, c in enumerate(text):
        for j in range(k, 0, -1):
            s[j] = ((s[j] << 1) | 1) & masks[ord(c)] | (s[j - 1] << 1) | 1
        s[0] = ((s[0] << 1) | 1) & masks[ord(c)]
        if nth_bit(s[k], m - 1) == 0:
            result.append(i - m + 1)
    return result