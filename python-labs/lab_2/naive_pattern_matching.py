def naive_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the naive pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # This is the most straightforward approach to string matching:
    # 1. Check every possible starting position in the text
    # 2. For each position, compare the pattern with the text character by character
    # 3. If all characters match, add the starting position to the results
    # 4. Handle edge cases like empty patterns and patterns longer than the text

    n = len(text)
    m = len(pattern)
    if n == 0 or m == 0:
        return []
    if m > n:
        return []

    result: list[int] = []
    for i, _ in enumerate(text):
        if i + m > n:
            break
        if text[i:i+len(pattern)] == pattern:
            result.append(i)

    return result