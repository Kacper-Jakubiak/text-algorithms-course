def compute_hash(s: str, base: int, prime: int) -> int:
    result = 0
    for char in s:
        result = (result * base + ord(char)) % prime
    return result

def rabin_karp_pattern_match(text: str, pattern: str, prime: int = 101) -> list[int]:
    """
    Implementation of the Rabin-Karp pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for
        prime: A prime number used for the hash function

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # This algorithm uses hashing to find pattern matches:
    # 1. Compute the hash value of the pattern
    # 2. Compute the hash value of each text window of length equal to pattern length
    # 3. If the hash values match, verify character by character to avoid hash collisions
    # 4. Use rolling hash to efficiently compute hash values of text windows
    # 5. Return all positions where the pattern is found in the text
    # Note: Use the provided prime parameter for the hash function to avoid collisions
    n = len(text)
    m = len(pattern)
    if n == 0 or m == 0 or m > n:
        return []

    base = 256
    big = pow(base, m-1, prime)

    result = []
    pattern_hash = compute_hash(pattern, base, prime)
    rolling = compute_hash(text[:m], base, prime)

    k = 0
    while k + m < n:
        if rolling == pattern_hash:
            if text[k:k+m] == pattern:
                result.append(k)
        subtractor = (big * ord(text[k])) % prime
        adder = ord(text[k + m]) % prime
        rolling = rolling - subtractor + prime
        rolling = (rolling * base) % prime
        rolling = (rolling + adder) % prime
        k += 1

    if rolling == pattern_hash:
        if text[k:k + m] == pattern:
            result.append(k)

    return result

if __name__ == "__main__":
    wyn = rabin_karp_pattern_match('barbara', 'ba')
    print(f'{wyn}')