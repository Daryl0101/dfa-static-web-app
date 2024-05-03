# References https://blog.devgenius.io/finite-automata-implement-a-dfa-in-python-64dc3d7005d9
class DFA:
    # 5-tuple init
    def __init__(
        self, alphabets, states, transition_functions, initial_state, final_states
    ):
        self.alphabets = alphabets
        self.states = states
        self.transitions = transition_functions
        self.initial_state = initial_state
        self.final_states = final_states

    # Processes the input word and returns True if the word is accepted by the DFA
    def is_accepting(self, input_string: str):
        current_state = self.initial_state

        for char in input_string:
            if char not in self.alphabets:
                return False

            current_state = self.transitions.get(current_state, {}).get(char, None)
            if current_state is None:
                return False

        return current_state in self.final_states

    # Processes the input paragraph and returns a dictionary of accepted words and their positions
    def check(self, paragraph: str):
        # Reject empty input
        if paragraph.strip() == "":
            raise ValueError("Empty string provided")

        # Normalize the input
        paragraph = paragraph.lower().strip()

        # Convert the paragraph to a list of characters
        chars = list(paragraph)

        current_word = ""
        accepted_words: dict[str : list[tuple[int, int]]] = (
            {}
        )  # returns: {word: [(start_index, end_index)]}

        # Start and end index of the current word
        word_start = 0
        word_end = 0

        # Traverse the characters in the paragraph
        for i, char in enumerate(chars):
            # If the character is in the alphabet, then it is part of the word
            if char in self.alphabets:
                current_word += char
                word_end = i

            # If the character is not in the alphabet or it is the last character in the paragraph
            # then the current word is complete
            # Check if the current word is accepted by the DFA
            # If it is accepted, add it to the accepted_words dictionary
            # Reset the current_word to an empty string
            if char not in self.alphabets or i == len(chars) - 1:
                if current_word != "":
                    if self.is_accepting(current_word):
                        accepted_words[current_word] = accepted_words.get(
                            current_word, []
                        ) + [(word_start, word_end)]
                    current_word = ""
                word_start = i + 1

        return accepted_words


# Generate a DFA from a list of words
def generate_dfa(input_strings: list[str]) -> DFA:
    alphabets = {
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
    transition_functions = {}
    final_states = set()

    for input_string in [
        input_string.lower().strip() for input_string in input_strings
    ]:

        current_state = 0

        for i in input_string:

            if i not in alphabets:
                raise ValueError(f"Invalid character '{i}' in string '{input_string}'")

            # Find the upcoming state based on the current state and the input character to reach the next state
            upcoming_state = transition_functions.get(current_state)
            if upcoming_state is not None:
                upcoming_state = upcoming_state.get(i)

            # Create a new state if the upcoming state is not found
            if upcoming_state is None:
                # The new state is the next integer after the maximum state in the set of states
                upcoming_state = len(states)
                # Add the new state to the set of states
                states.add(upcoming_state)
                # Add the transition into the transition functions dictionary
                if current_state not in transition_functions:
                    transition_functions[current_state] = {}
                transition_functions[current_state][i] = upcoming_state

            # Move to the upcoming state
            current_state = upcoming_state

        # Add the final state to the set of final states
        final_states.add(current_state)

    return DFA(alphabets, states, transition_functions, 0, final_states)
