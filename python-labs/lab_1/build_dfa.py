from abc import ABC, abstractmethod
from collections import deque
from typing import Optional


class RegEx(ABC):
    @abstractmethod
    def nullable(self):
        pass

    @abstractmethod
    def derivative(self, symbol):
        pass

    def __eq__(self, other):
        if not isinstance(other, RegEx):
            return False
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


class Empty(RegEx):
    def nullable(self):
        return False

    def derivative(self, symbol):
        return Empty()

    def __str__(self):
        return "∅"


class Epsilon(RegEx):
    def nullable(self):
        return True

    def derivative(self, symbol):
        return Empty()

    def __str__(self):
        return "ε"


class Symbol(RegEx):
    def __init__(self, symbol):
        self.symbol = symbol

    def nullable(self):
        return False

    def derivative(self, symbol):
        if self.symbol == symbol:
            return Epsilon()
        return Empty()

    def __str__(self):
        return self.symbol


class Concatenation(RegEx):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def nullable(self):
        return self.left.nullable() and self.right.nullable()

    def derivative(self, symbol):
        left_derivative = self.left.derivative(symbol)

        if isinstance(left_derivative, Empty):
            if self.left.nullable():
                return self.right.derivative(symbol)
            return Empty()

        if self.left.nullable():
            right_derivative = self.right.derivative(symbol)
            if isinstance(right_derivative, Empty):
                return Concatenation(left_derivative, self.right)
            return Alternative(
                Concatenation(left_derivative, self.right), right_derivative
            )
        else:
            return Concatenation(left_derivative, self.right)

    def __str__(self):
        return f"({self.left}{self.right})"


class Alternative(RegEx):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def nullable(self):
        return self.left.nullable() or self.right.nullable()

    def derivative(self, symbol):
        left_derivative = self.left.derivative(symbol)
        right_derivative = self.right.derivative(symbol)

        if isinstance(left_derivative, Empty):
            return right_derivative
        if isinstance(right_derivative, Empty):
            return left_derivative

        return Alternative(left_derivative, right_derivative)

    def __str__(self):
        return f"({self.left}|{self.right})"


class KleeneStar(RegEx):
    def __init__(self, expression):
        self.expression = expression

    def nullable(self):
        return True

    def derivative(self, symbol):
        derivative = self.expression.derivative(symbol)

        if isinstance(derivative, Empty):
            return Empty()

        return Concatenation(derivative, self)

    def __str__(self):
        return f"({self.expression})*"


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, string):
        """Check if the DFA accepts the given string."""
        current_state = self.start_state

        for i, symbol in enumerate(string):
            if symbol not in self.alphabet:
                return False

            if (current_state, symbol) not in self.transitions:
                return False

            current_state = self.transitions[(current_state, symbol)]

        return current_state in self.accept_states

    def __str__(self):
        result = "DFA:\n"
        result += f"  States: {self.states}\n"
        result += f"  Alphabet: {self.alphabet}\n"
        result += f"  Start State: {self.start_state}\n"
        result += f"  Accept States: {self.accept_states}\n"
        result += "  Transitions:\n"
        for (state, symbol), next_state in sorted(self.transitions.items()):
            result += f"    {state} --{symbol}--> {next_state}\n"
        return result


def simplify(regex):
    """
    Simplify regex expressions to canonical form to improve state identification.
    """
    if (
        isinstance(regex, Empty)
        or isinstance(regex, Epsilon)
        or isinstance(regex, Symbol)
    ):
        return regex

    # For alternatives
    if isinstance(regex, Alternative):
        left = simplify(regex.left)
        right = simplify(regex.right)

        if isinstance(left, Empty):
            return right
        if isinstance(right, Empty):
            return left

        if str(left) == str(right):
            return left

        return Alternative(left, right)

    # For concatenations
    if isinstance(regex, Concatenation):
        left = simplify(regex.left)
        right = simplify(regex.right)

        if isinstance(left, Empty) or isinstance(right, Empty):
            return Empty()

        if isinstance(left, Epsilon):
            return right

        if isinstance(right, Epsilon):
            return left

        return Concatenation(left, right)

    # For Kleene star
    if isinstance(regex, KleeneStar):
        inner = simplify(regex.expression)

        if isinstance(inner, KleeneStar):
            return inner

        if isinstance(inner, Epsilon):
            return Epsilon()

        if isinstance(inner, Empty):
            return Epsilon()

        return KleeneStar(inner)

    return regex


def build_dfa(regex: RegEx, alphabet: set[str]) -> Optional[DFA]:
    states: set[str] = set()  # Set of state names (q0, q1, etc.)
    state_to_regex: dict[str, RegEx] = {}  # Maps state names to their regex
    accept_states: set[str] = set()  # Set of accepting state names
    transitions: dict[tuple[str, str], str] = {}  # Maps (state, symbol) pairs to next state
    regex_to_state: dict[str, str] = {}  # Maps string representations of regex to state names

    state_counter = 0
    q: deque[str] = deque() # kolejka na stany

    def next_name() -> str:
        # łatwiejsze nazywanie stanów
        nonlocal state_counter
        state_counter += 1
        return f"q{state_counter-1}"

    start_state: str = next_name()
    states.add(start_state)
    state_to_regex[start_state] = regex
    regex_to_state[str(regex)] = start_state
    if regex.nullable():
        accept_states.add(start_state)
    q.append(start_state)

    while q:
        current_state: str = q.popleft()
        current_regex: RegEx = state_to_regex[current_state]
        for symbol in alphabet:
            # dla każdego symbolu alfabetu
            next_regex: RegEx = simplify(current_regex.derivative(symbol))
            # znajdujemy następny regex
            if isinstance(next_regex, Empty):
                continue
                # pomijamy puste (brak dopasowania)
            next_regex_str = str(next_regex)
            if next_regex_str in regex_to_state.keys():
                # gdy już istnieje ten stan to tylko dodajemy tranzycję
                transitions[(current_state, symbol)] = regex_to_state[next_regex_str]
                continue
            next_state: str = next_name()
            states.add(next_state)
            state_to_regex[next_state] = next_regex
            regex_to_state[next_regex_str] = next_state
            transitions[(current_state, symbol)] = next_state
            # dodajemy nowy regex do wszystkich struktur
            if next_regex.nullable():
                accept_states.add(next_state)
                # sprawdzamy, czy jest to stan akceptujący
            q.append(next_state)
            #dodajemy na kolejkę przetworzony stan

    return DFA(states, alphabet, transitions, start_state, accept_states)