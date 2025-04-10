def compute_lps_array(pattern: str) -> list[int]:
    """
    Compute the Longest Proper Prefix which is also Suffix array for KMP algorithm.

    Args:
        pattern: The pattern string

    Returns:
        The LPS array
    """
    # The LPS array helps in determining how many characters to skip when a mismatch occurs
    # For each position i, compute the length of the longest proper prefix of pattern[0...i]
    # that is also a suffix of pattern[0...i]
    # Hint: Use the information from previously computed values to avoid redundant comparisons
    m = len(pattern)
    lps = [0] * m
    i = 1
    longest = 0
    while i < m:
        if pattern[i] == pattern[longest]:
            longest += 1
            lps[i] = longest
            i += 1
        else:
            if longest != 0:
                longest = lps[longest - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Knuth-Morris-Pratt pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # 1. Preprocess the pattern to compute the LPS array
    # 2. Use the LPS array to determine how much to shift the pattern when a mismatch occurs
    # 3. This avoids redundant comparisons by using information about previous matches
    # 4. Return all positions where the pattern is found in the text
    lps = compute_lps_array(pattern)
    result = []
    n = len(text)
    m = len(pattern)
    if m == 0 or n < m:
        return []

    i = 0
    j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return result

if __name__ == '__main__':
    wzor = "ABABACA"
    tablice = compute_lps_array(wzor)
    print(list(wzor))
    print(tablice)