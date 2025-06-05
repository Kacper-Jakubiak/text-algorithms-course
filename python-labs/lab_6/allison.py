def allison_global_alignment(s1: str, s2: str,
                             match_score: int = 2,
                             mismatch_score: int = -1,
                             gap_penalty: int = -1) -> tuple[int, str, str]:
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
            match = dp[i - 1][j - 1] + (match_score if s1[i - 1] == s2[j - 1] else mismatch_score)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            dp[i][j] = max(match, delete, insert)

    # Śledzenie wyrównania
    aligned_s1 = []
    aligned_s2 = []
    i, j = n, m
    while i > 0 or j > 0:
        current = dp[i][j]
        if i > 0 and j > 0 and current == dp[i - 1][j - 1] + (
        match_score if s1[i - 1] == s2[j - 1] else mismatch_score):
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and current == dp[i - 1][j] + gap_penalty:
            aligned_s1.append(s1[i - 1])
            aligned_s2.append('-')
            i -= 1
        else:
            aligned_s1.append('-')
            aligned_s2.append(s2[j - 1])
            j -= 1

    return dp[n][m], ''.join(reversed(aligned_s1)), ''.join(reversed(aligned_s2))


def allison_local_alignment(s1: str, s2: str,
                            match_score: int = 2,
                            mismatch_score: int = -1,
                            gap_penalty: int = -1) -> tuple[int, str, str, int, int]:
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_score = 0
    max_pos = (0, 0)

    # Wypełnianie macierzy
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i - 1][j - 1] + (match_score if s1[i - 1] == s2[j - 1] else mismatch_score)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            dp[i][j] = max(0, match, delete, insert)
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_pos = (i, j)

    # Śledzenie wyrównania od punktu max_pos
    i, j = max_pos
    aligned_s1 = []
    aligned_s2 = []
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

    return max_score, ''.join(reversed(aligned_s1)), ''.join(reversed(aligned_s2)), i, j
