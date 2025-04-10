import os
import re
from collections import Counter

def analyze_text_file(filename: str) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        return {"error": f"Could not read file: {str(e)}"}

    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "with",
        "by",
        "about",
        "as",
        "into",
        "like",
        "through",
        "after",
        "over",
        "between",
        "out",
        "of",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "from",
        "there",
        "their",
    }

    words = []
    for word in re.finditer(r"(?P<word>\b[\w./\-@]+\b)", content):
        words.append(word.group("word").lower())
    # Szukamy znaków \w oraz kilku innych występujących w datach i mailach,
    # aby traktować je jako jedno słowo. Rozdzielamy używając \b - word boundary
    # Dodajemy zmienione na lowercase
    word_count = len(words)

    sentence_pattern = r".*?[.!?](?=\s)"
    # Traktujemy zdanie jako ciąg znaków zakończonych [.!?] i białym znakiem
    # nie udało się znaleźć żadnego rozróżnienia bez patrzenia na znaczenie słów między:
    # Ala idzie do Jasia. Mama gotuje obiad.
    # Ala idzie do Dr. Małgorzaty po obiad.
    # Więc oba powyższe przykłady zostaną potraktowane jako dwa zdania
    sentences = []
    for sentence in re.finditer(sentence_pattern, content):
        sentences.append(sentence.group())
    sentence_count = len([s for s in sentences if s.strip()])


    email_pattern = r"[\w]\S*@\S*[\w]"
    # traktujemy email jako dowolny ciąg niebiałych znaków z @ w środku
    # zaczynający i kończący się znakiem "słownym" \w
    emails = [email.group() for email in re.finditer(email_pattern, content)]

    frequent_words = {}
    word_counter = Counter(words)
    # używamy Counter()
    for word in word_counter:
        if word in stop_words: # pomijamy stop_words
            continue
        if len(word) <= 1: # pomijamy krótkie słowa
            continue
        if word_counter[word] <= 1: # nie dodajemy słów, które występują tylko raz
            continue
        frequent_words[word] = int(word_counter[word])

    month = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b"
    # miesiące oraz ich 3-literowe skróty
    date_patterns = [
        r"\d{4}[\-._,/ ]\d{2}[\-._,/ ]\d{2}", # YYYY MM DD
        r"\d{2}[\-._,/ ]\d{2}[\-._,/ ]\d{4}", # DD MM YYYY
        # oba powyższe wzorce zakładają, że podział między
        # liczbami w dacie może być za pomocą dowolnego znaku z
        # [\-._,/ ]
        month + r" \d\d?, \d{4}" # słowne podanie miesiąca
    ]

    dates = []
    for date_pattern in date_patterns:
        for date in re.finditer(date_pattern, content):
            dates.append(date.group())

    paragraphs = re.split(r"\n\s*\n", content)
    paragraph_sizes = {}
    for i, paragraph in enumerate(paragraphs):
        paragraph_sizes[i] = len([word for word in re.finditer(r"(?P<word>\b[\w./\-@]+\b)", paragraph)])
        # używamy tego samego wzorca słów co w podliczaniu wszystkich słów

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "emails": emails,
        "frequent_words": frequent_words,
        "dates": dates,
        "paragraph_sizes": paragraph_sizes,
    }