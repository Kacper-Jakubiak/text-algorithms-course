def len_of_common_prefix(str1: str, str2: str) -> int:
    for k in range(min(len(str1), len(str2))):
        if str1[k] != str2[k]:
            return k
    return min(len(str1), len(str2))

def compute_z_array(s: str) -> list[int]:
    n = len(s)
    z_array = [0] * n
    # z_array[0] = n
    left, right = 0, 0
    for k in range(1, n):
        if k > right:
            z_array[k] = len_of_common_prefix(s, s[k:])
            if z_array[k] > 0:
                left, right = k, k + z_array[k]
        elif z_array[k-left] >= right-k:
            z_array[k] = right - k + len_of_common_prefix(s[right:], s[right-k:])
            left, right = k, k + z_array[k]
        else:
            z_array[k] = z_array[k-left]
    return z_array

def compute_lps_array(pattern: str) -> list[int]:
    """
    Compute the Longest Proper Prefix which is also Suffix array for KMP algorithm.

    Args:
        pattern: The pattern string

    Returns:
        The LPS array
    """
    # TODO: Implement the Longest Prefix Suffix (LPS) array computation
    # The LPS array helps in determining how many characters to skip when a mismatch occurs
    # For each position i, compute the length of the longest proper prefix of pattern[0...i]
    # that is also a suffix of pattern[0...i]
    # Hint: Use the information from previously computed values to avoid redundant comparisons
    z_array = compute_z_array(pattern)
    m = len(pattern)
    p = [0] * (m+1)
    for j in range(m-1, 0, -1):
        p[j + z_array[j]] = z_array[j]

    return p


def kmp_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Knuth-Morris-Pratt pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # TODO: Implement the KMP string matching algorithm
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

    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            # Match found
            result.append(i - j)
            j = lps[j - 1]  # Continue searching for next match

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]  # Fallback in the pattern
            else:
                i += 1  # Move to the next character in text

    return result

if __name__ == '__main__':
    wzor = "AAAA"
    tablice = compute_lps_array(wzor)
    print(list(wzor))
    print(tablice)