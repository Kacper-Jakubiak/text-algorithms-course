def allison_global_alignment(s1: str, s2: str,
                             match_score: int = 2,
                             mismatch_score: int = -1,
                             gap_penalty: int = -1) -> tuple[int, str, str]:
    """
    Znajduje optymalne globalne wyrównanie używając algorytmu Allisona.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania i dwa wyrównane ciągi
    """
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Inicjalizacja macierzy
    for i in range(n + 1):
        dp[i][0] = i * gap_penalty
    for j in range(m + 1):
        dp[0][j] = j * gap_penalty

    # Wypełnianie macierzy
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # liczymy wszystkie opcje, typowe dla algorytmów dynamicznych
            match = dp[i - 1][j - 1] + (match_score if s1[i - 1] == s2[j - 1] else mismatch_score)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            # wybieramy najepszą opcję
            dp[i][j] = max(match, delete, insert)

    # zdobycie stringów z macierzy kroków
    aligned_s1 = []
    aligned_s2 = []
    # zaczynamy na końcu
    i, j = n, m
    # cofamy się aż nie dojdziemy do (0, 0)
    while i > 0 or j > 0:
        current = dp[i][j]
        # sprawdzamy czy przyszliśmy z "ukosu"
        if i > 0 and j > 0 and current == dp[i - 1][j - 1] + (
                match_score if s1[i - 1] == s2[j - 1] else mismatch_score):
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(s2[j - 1])
            i -= 1
            j -= 1
        # z jednej strony
        elif i > 0 and current == dp[i - 1][j] + gap_penalty:
            aligned_s1.append(s1[i - 1])
            aligned_s2.append('-')
            i -= 1
        # lub z drugiej strony
        else:
            aligned_s1.append('-')
            aligned_s2.append(s2[j - 1])
            j -= 1

    # przez to że tworzymy stringi od tyłu to trzeba dać reverse
    return dp[n][m], ''.join(reversed(aligned_s1)), ''.join(reversed(aligned_s2))


def allison_local_alignment(s1: str, s2: str,
                            match_score: int = 2,
                            mismatch_score: int = -1,
                            gap_penalty: int = -1) -> tuple[int, str, str, int, int]:
    """
    Znajduje optymalne lokalne wyrównanie (podobnie do algorytmu Smith-Waterman).

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania, dwa wyrównane ciągi oraz pozycje początku
    """
    # to samo co dla global, tylko nie obchodzą nas ujemne wartości, więc szukamy maksa
    # zakładając że w każdej chwili możemy uciąć początki tekstów
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_score = 0
    # trzymamy pozycję dla celów zdobycia stringów
    max_pos = (0, 0)

    # Wypełnianie macierzy
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # to samo co dla global
            match = dp[i - 1][j - 1] + (match_score if s1[i - 1] == s2[j - 1] else mismatch_score)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            # to samo co dla global tylko nie trzymamy ujemnych, zawsze można po prostu "uciąć" cały początek
            # i uzyskać wynik 0
            dp[i][j] = max(0, match, delete, insert)
            # aktualizujemy max
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_pos = (i, j)

    # Śledzenie wyrównania od punktu max_pos
    # zaczynamy tam gdzie znaleziony został max
    i, j = max_pos
    aligned_s1 = []
    aligned_s2 = []
    # identyczna pętla co dla global, kończymy jak dojdziemy na start lub do 0,
    # wtedy można "zachłannie" skończyć, bo nie ważne od jakiego 0 zaczeliśmy
    while i > 0 and j > 0 and dp[i][j] != 0:
        if dp[i][j] == dp[i - 1][j - 1] + (match_score if s1[i - 1] == s2[j - 1] else mismatch_score):
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + gap_penalty:
            aligned_s1.append(s1[i - 1])
            aligned_s2.append('-')
            i -= 1
        else:
            aligned_s1.append('-')
            aligned_s2.append(s2[j - 1])
            j -= 1

    # to samo co dla global, tylko jeszcze zwracamy skąd zaczynamy oba stringi
    return max_score, ''.join(reversed(aligned_s1)), ''.join(reversed(aligned_s2)), i, j
