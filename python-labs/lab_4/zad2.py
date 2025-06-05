## Zadanie 2: Rozszerzone Problemy z Najdłuższymi Wspólnymi Podciągami (2 pkt)
import random
import string
from time import perf_counter as pf

from matplotlib import pyplot as plt

# Zaimplementuj funkcje rozwiązujące następujące problemy związane z najdłuższymi wspólnymi podciągami, wykorzystując struktury sufiksowe:
from ukkonen import SuffixTree


def longest_common_substring_tree(str1: str, str2: str) -> str:
    """
    Find the longest common substring of two strings using a suffix tree.

    Args:
        str1: First string
        str2: Second string

    Returns:
        The longest common substring
    """
    # Concatenate the strings with a unique separator
    combined = str1 + "#" + str2 + "$"

    # Build a suffix tree for the combined string
    # Traverse the tree to find the longest path that occurs in both strings
    tree = SuffixTree(combined)

    # return longest_substring


def longest_common_substring_array(str1: str, str2: str) -> str:
    pass


def longest_common_substring_multiple(strings: list[str]) -> str:
    """
    Find the longest common substring among multiple strings using suffix structures.

    Args:
        strings: List of strings to compare

    Returns:
        The longest common substring that appears in all strings
    """
    # Implement an algorithm to find the longest common substring in multiple strings
    # You may use either suffix trees or suffix arrays

    pass


def longest_palindromic_substring(text: str) -> str:
    """
    Find the longest palindromic substring in a given text using suffix structures.

    Args:
        text: Input text

    Returns:
        The longest palindromic substring
    """
    # Create a new string concatenating the original text and its reverse
    # Use suffix structures to find the longest common substring between them
    # Handle the case where palindrome centers between characters

    pass


def common():
    results = []
    lengths = [100, 1000, 10000, 100000]
    for length in lengths:
        t1 = ''.join(random.choices(string.ascii_lowercase, k=length))
        t2 = ''.join(random.choices(string.ascii_lowercase, k=length))
        start = pf()
        longest_common_substring_tree(t1, t2)
        stop = pf()
        tree_time = stop - start
        start = pf()
        longest_common_substring_array(t1, t2)
        stop = pf()
        array_time = stop - start
        results.append((tree_time * 1000, array_time * 1000))

    plt.plot((2, 3, 4, 5), [r[0] for r in results], 'o', label='array')
    plt.plot((2, 3, 4, 5), [r[1] for r in results], 'o', label='tree')
    plt.title("zadanie 2 porównanie czasu")
    plt.legend()
    plt.savefig(f'zad2.png')
    plt.show()


if __name__ == "__main__":
    common()

# Dla każdej z tych funkcji:
# 1. Zaimplementuj rozwiązanie wykorzystujące odpowiednią strukturę sufiksową (drzewo sufiksów lub tablicę sufiksów)
# 2. Przeanalizuj złożoność czasową i pamięciową
# 3. Przetestuj na różnych zbiorach danych, w tym przypadkach brzegowych
# 4. Porównaj wydajność Twojego rozwiązania z podejściami wykorzystującymi inne algorytmy (np. programowanie dynamiczne)
#
# Utwórz wykres porównujący czas wykonania algoritmu najdłuższego wspólnego podciągu dla dwóch ciągów znaków w zależności od długości ciągów, używając drzewa sufiksowego, tablicy sufiksów oraz dowolnego innego algorytmu.
#
# **Podpowiedź**: Problem najdłuższego wspólnego podciągu dla wielu ciągów znaków jest znacznie trudniejszy niż dla dwóch ciągów. Zastanów się, jak można zmodyfikować podstawowy algorytm, aby uwzględnić większą liczbę ciągów. Dla problemu najdłuższego palindromicznego podciągu, rozważ, jak można wykorzystać właściwości palindromów w połączeniu ze strukturami sufiksowymi.
