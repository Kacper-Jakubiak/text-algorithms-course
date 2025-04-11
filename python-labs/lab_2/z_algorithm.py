def len_of_common_prefix(str1: str, str2: str) -> int:
    for k in range(min(len(str1), len(str2))):
        if str1[k] != str2[k]:
            return k
    return min(len(str1), len(str2))

def compute_z_array(s: str) -> list[int]:
    """
    Compute the Z array for a string.

    The Z array Z[i] gives the length of the longest substring starting at position i
    that is also a prefix of the string.

    Args:
        s: The input string

    Returns:
        The Z array for the string
    """
    # For each position i:
    # - Calculate the length of the longest substring starting at i that is also a prefix of s
    # - Use the Z-box technique to avoid redundant character comparisons
    # - Handle the cases when i is inside or outside the current Z-box
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


def z_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Use the Z algorithm to find all occurrences of a pattern in a text.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # 1. Create a concatenated string: pattern + special_character + text
    # 2. Compute the Z array for this concatenated string
    # 3. Find positions where Z[i] equals the pattern length
    # 4. Convert these positions in the concatenated string to positions in the original text
    # 5. Return all positions where the pattern is found in the text
    n = len(text)
    m = len(pattern)
    if n == 0 or m == 0 or m > n:
        return []

    final = pattern + '$' + text
    z_array = compute_z_array(final)

    result: list[int] = []
    for i, value in enumerate(z_array):
        if value != m:
            continue
        if i - m - 1 >= 0:
            result.append(i - m - 1)

    return result