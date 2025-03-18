# Wyrażenia regularne


### Zadanie 1: Ekstrakcja informacji z publikacji naukowych - `parse_publication` (2 pkt)

Dane są referencje publikacji naukowych w formacie:
Nazwisko, I., Nazwisko2, I2. (Rok). Tytuł publikacji. Nazwa czasopisma, Tom(Numer), strony.

Na przykład:
Kowalski, J., Nowak, A. (2023). Analiza algorytmów tekstowych. Journal of Computer Science, 45(2), 123-145.

Napisz funkcję parse_publication, która dla podanej referencji zwraca słownik zawierający:
- listę autorów (każdy autor jako słownik {'last_name': nazwisko, 'initial': inicjał})
- rok publikacji
- tytuł
- czasopismo
- tom
- numer (jeśli istnieje, w przeciwnym razie None)
- zakres stron (jako słownik {'start': pierwsza_strona, 'end': ostatnia_strona})

### Zadanie 2: Analiza linków w kodzie HTML - `extract_links` (2 pkt)

Napisz funkcję extract_links, która dla podanego fragmentu kodu HTML wyodrębnia wszystkie linki.
Funkcja powinna zwracać listę słowników, gdzie każdy słownik zawiera:
- url: adres docelowy linku (wartość atrybutu `href`)
- text: tekst wyświetlany jako link (tekst pomiędzy `<a> i </a>`)
- title: tytuł linku (wartość atrybutu title, jeśli istnieje, w przeciwnym razie `None`)

Przykład:

```
html = '<div><a href="https://www.agh.edu.pl">AGH</a> <a href="https://www.agh.edu.pl/wydzialy" title="Wydziały">Wydziały AGH</a></div>'
extract_links(html) 
-> [
    {'url': 'https://www.agh.edu.pl', 'text': 'AGH', 'title': None},
    {'url': 'https://www.agh.edu.pl/wydzialy', 'text': 'Wydziały AGH', 'title': 'Wydziały'}
]
```


### Zadanie 3: Analiza pliku tekstowego - `analyze_text_file` (3 pkt)

Napisz funkcję analyze_text_file, która analizuje podany plik tekstowy i zwraca słownik zawierający:
- `word_count`: całkowitą liczbę słów
- `sentence_count`: liczbę zdań
- `emails`: listę znalezionych adresów e-mail
- `frequent_words`: 10 najczęściej występujących słów (bez słów stopowych)
- `dates`: listę znalezionych dat w różnych formatach
- `paragraph_sizes`: słownik określający liczbę słów w każdym paragrafie


### Zadanie 4: Implementacja uproszczonego parsera regexpów `build_dfa` (3 pkt)

Zaimplementuj uproszczony parser wyrażeń regularnych, który konwertuje proste wyrażenia regularne do deterministycznego automatu skończonego (DFA) wykorzystując algorytm Brzozowskiego z pochodnych wyrażeń regularnych.

Twój parser powinien obsługiwać:
- Symbole literalne (a, b, c, ...)
- Konkatenację wyrażeń (ab)
- Alternatywę wyrażeń (a|b)
- Gwiazdkę Kleene'a (a*)

Napisz następujące funkcje:
1. `derivative(regex, symbol)` - oblicza pochodną Brzozowskiego wyrażenia regularnego względem symbolu
2. `accepts(regex, string)` - sprawdza, czy łańcuch pasuje do wyrażenia regularnego
3. `build_dfa(regex, alphabet)` - buduje DFA dla danego wyrażenia regularnego i alfabetu

Reprezentacja wyrażeń regularnych powinna używać klas:
- Symbol - dla pojedynczego symbolu
- Concatenation - dla konkatenacji wyrażeń
- Alternative - dla alternatywy wyrażeń
- KleeneStar - dla gwiazdki Kleene'a
- Epsilon - dla pustego łańcucha
- Empty - dla pustego zbioru

Przykład użycia:
```python
# Wyrażenie regularne: (a|b)*abb
regex = Concatenation(
    Concatenation(
        Concatenation(
            KleeneStar(Alternative(Symbol('a'), Symbol('b'))),
            Symbol('a')
        ),
        Symbol('b')
    ),
    Symbol('b')
)

# Sprawdzenie, czy łańcuch pasuje do wyrażenia
assert accepts(regex, "abb") == True
assert accepts(regex, "aabb") == True
assert accepts(regex, "babb") == True
assert accepts(regex, "ab") == False

# Budowa DFA
dfa = build_dfa(regex, ['a', 'b'])
```

Wskazówki:
- Użyj rekurencji do implementacji pochodnej Brzozowskiego
- Pamiętaj o zasadach obliczania pochodnej dla różnych rodzajów wyrażeń
- Możesz użyć metody __eq__ i __hash__ do porównywania i haszowania wyrażeń regularnych
