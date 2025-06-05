## Zadanie 3: Tablica Sufiksów vs. Drzewo Sufiksów (2 pkt)
import random
import string
import tracemalloc
from time import perf_counter as pf

from matplotlib import pyplot as plt

from ukkonen import SuffixTree


# Zaimplementuj obie struktury danych - tablicę sufiksów i drzewo sufiksów - dla tego samego tekstu, a następnie porównaj ich zużycie pamięci i czas konstrukcji.

def make_suffix_array(text: str) -> list[int]:
    return [1]


def compare_suffix_structures(text: str) -> dict:
    """
    Compare suffix array and suffix tree data structures.

    Args:
        text: The input text for which to build the structures

    Returns:
        A dictionary containing:
        - Construction time for both structures
        - Memory usage for both structures
        - Size (number of nodes/elements) of both structures
    """
    # Implement suffix array construction
    start = pf()
    tracemalloc.start()
    array = make_suffix_array(text)
    _, array_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = pf()
    array_time = end - start

    # Use suffix tree construction using Ukkonen's algorithm
    start = pf()
    tracemalloc.start()
    tree = SuffixTree(text)
    _, tree_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = pf()
    tree_time = end - start

    # Measure and compare metrics

    return {
        "suffix_array": {
            "construction_time_ms": array_time * 1000,
            "memory_usage_kb": array_mem / 1024,
            "size": len(array)
        },
        "suffix_tree": {
            "construction_time_ms": tree_time * 1000,
            "memory_usage_kb": tree_mem / 1024,
            "size": tree.size
        }
    }


def main():
    results = []
    lengths = [100, 1000, 10000, 100000]
    for length in lengths:
        text = ''.join(random.choices(string.ascii_lowercase, k=length))
        results.append(compare_suffix_structures(text))

    plots = ["construction_time_ms", "memory_usage_kb", "size"]
    for title in plots:
        plt.plot((2, 3, 4, 5), [r["suffix_array"][title] for r in results], 'o', label='array')
        plt.plot((2, 3, 4, 5), [r["suffix_tree"][title] for r in results], 'o', label='tree')
        plt.title(title)
        plt.legend()
        plt.savefig(f'zad4_{title}.png')
        plt.show()


if __name__ == '__main__':
    main()
# Przeanalizuj, jak te metryki skalują się wraz z rozmiarem tekstu, testując na tekstach o różnej długości (np. 100, 1000, 10000, 100000 znaków).
#
# **Ważne:** Utwórz szczegółowe wykresy pokazujące:
# 1. Czas konstrukcji w zależności od rozmiaru tekstu
# 2. Zużycie pamięci w zależności od rozmiaru tekstu
# 3. Rozmiar (liczba elementów) w zależności od rozmiaru tekstu
#
# Użyj odpowiednich skal i upewnij się, że wykresy wyraźnie ilustrują różnice w charakterystykach wydajności. Wyjaśnij, w jakich scenariuszach preferowałbyś tablice sufiksów zamiast drzew sufiksów i odwrotnie.
