## Zadanie 4: Analiza Porównawcza Algorytmów Dopasowywania Wzorców (3 pkt)

# Zaimplementuj następujące algorytmy dopasowywania wzorców (lub użyj tych, które zostały zaimplementowane w poprzednich laboratoriach):
#
# 1. Naiwny algorytm dopasowywania wzorców
# 2. Algorytm KMP (Knutha-Morrisa-Pratta)
# 3. Algorytm Boyer-Moore
# 4. Algorytm Rabin-Karp
# 5. Algorytm Aho-Corasick (dla wyszukiwania wielu wzorców jednocześnie)
# 6. Wyszukiwanie oparte na tablicy sufiksów
# 7. Wyszukiwanie oparte na drzewie sufiksów (z wykorzystaniem implementacji algorytmu Ukkonena)
#
# Następnie stwórz funkcję, która porównuje ich wydajność:

def compare_pattern_matching_algorithms(text: str, pattern: str) -> dict:
    """
    Compare the performance of different pattern matching algorithms.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A dictionary containing the results of each algorithm:
        - Execution time in milliseconds
        - Memory usage in kilobytes
        - Number of character comparisons made
        - Positions where the pattern was found
    """
    results = {}

    # Implement algorithm comparisons
    # For each algorithm:
    #   1. Measure execution time
    #   2. Measure memory usage
    #   3. Count character comparisons
    #   4. Find pattern positions

    return results

# Przetestuj algorytmy na tekstach o różnych rozmiarach i wzorcach o różnej długości.
#
# **Ważne:** Utwórz szczegółowe porównania wizualne przy użyciu odpowiednich wykresów dla:
# 1. Czasu wykonania w zależności od rozmiaru tekstu
# 2. Zużycia pamięci w zależności od rozmiaru tekstu
# 3. Liczby porównań w zależności od rozmiaru tekstu
# 4. Czasu wykonania w zależności od długości wzorca
#
# Użyj skal logarytmicznych tam, gdzie jest to odpowiednie, aby wyraźnie pokazać różnice między algorytmami. Wyjaśnij kompromisy między algorytmami na podstawie swoich wyników.
