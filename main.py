# References https://blog.devgenius.io/finite-automata-implement-a-dfa-in-python-64dc3d7005d9
class DFA:
    # 5-tuple init
    def __init__(self, alphabet, states, transitions, start_state, final_states):
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def is_accepting(self, input_string: str):
        current_state = self.start_state

        for char in input_string:
            if char not in self.alphabet:
                return False

            current_state = self.transitions.get(current_state, {}).get(char, None)
            if current_state is None:
                return False

        return current_state in self.final_states

    def check(self, paragraph: str):
        if paragraph.strip() == "":
            raise ValueError("Empty string provided")
        paragraph = paragraph.lower().strip()

        chars = list(paragraph)
        current_word = ""
        accepted_words: dict[list[tuple[int, int]]] = (
            {}
        )  # {word: [(start_index, end_index)]}
        word_start = 0
        word_end = 0
        for i, char in enumerate(chars):
            if char in self.alphabet:
                current_word += char
                word_end = i

            if char not in self.alphabet or i == len(chars) - 1:
                if current_word != "":
                    if self.is_accepting(current_word):
                        accepted_words[current_word] = accepted_words.get(
                            current_word, []
                        ) + [(word_start, word_end)]
                    current_word = ""
                word_start = i + 1

        return accepted_words


def generate_dfa(words: list[str]) -> DFA:
    alphabet = {
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    }
    states = set([0])
    transitions = {}
    start_state = 0
    final_states = set()

    for i, word in enumerate(words):
        current_state = 0
        for char in word:
            # Get the next state in the DFA of the current state based on the character available for transition
            next_state = transitions.get(current_state, {}).get(char, None)

            # If the next state is not in the DFA, then create one for it.
            if next_state is None:
                next_state = len(states)
                transitions.setdefault(current_state, {})[char] = next_state
                states.add(next_state)
            current_state = next_state
        final_states.add(current_state)

    return DFA(alphabet, states, transitions, start_state, final_states)


words = []
with open("words.txt") as file:
    words = file.readlines()
    words = [word.strip() for word in words]

dfa = generate_dfa(words)
print(dfa.check("...and the and the and ... and"))
