def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Levenshteina między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Levenshteina (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    if min(len(s1), len(s2)) == 0:
        return max(len(s1), len(s2))

    a = len(s1) + 1
    b = len(s2) + 1

    matrix = [[0] * b for _ in range(2)]
    for j in range(b):
        matrix[0][j] = j

    for i in range(1, a):
        matrix[i % 2][0] = i
        for j in range(1, b):
            matrix[i%2][j] = min(
                matrix[(i+1)%2][j] + 1,
                matrix[i%2][j-1] + 1,
                matrix[(i+1)%2][j-1] + (0 if s1[i-1] == s2[j-1] else 1)
            )

    return matrix[len(s1) % 2][len(s2)]

if __name__ == "__main__":
    levenshtein_distance('barbara', 'ba')