from state import State
from typing import Dict, List, Tuple

EPSILON = 'ε'


class NFA:
    """
    NFA
    Class to define the structure of an NFA with helper functions to help build it.
    """

    def __init__(self):
        self.initial_state: State = None
        self.accepting_states = []
        self.alphabet: List[str] = []
        self.states = []
        self.transition_function: Dict[(State, str), List[State]] = {}

    def initialize_nfa(self, regex: str) -> None:
        """
        initialize_nfa
        Initialize the NFA by adding an initial state and alphabet.

        :param regex: The regex to build the alphabet from.
        """

        # Convert to set to remove duplicate characters.
        self.alphabet = list(set([x for x in regex if x.isalnum()]))

        initial_state = State(len(self.states))
        self.states.append(initial_state)
        self.initial_state = initial_state

    def add_to_transition_function(self, transition: Tuple[State, str], state: State) -> None:
        """
        add_to_transition_function
        Insert a new transition to a state.

        :param transition: A tuple of a state and the input char.
        :param state: The ending state of the transition.
        """
        if transition in self.transition_function:
            self.transition_function[transition].append(state)
        else:
            self.transition_function[transition] = [state]

    def add_normal_char(self, old_state: State, transition_char: str, assume_accept: bool=True) -> State:
        """
        add_normal_char
        Add necessary states and transitions to connect one state to a new one on some character.
        Invariants: State is in self.states, char is in self.alphabet.
        Assume final state should be an accepting state unless told otherwise.

        :param old_state: The state to transition from.
        :param transition_char: The char to transition on.
        :param assume_accept: Whether to assume final state is accepting or not.
        :return: The state representing the final state of this sequence.
        """
        # Build a new state to transition to
        new_state = State(len(self.states))

        # Add state to states
        self.states.append(new_state)

        # Add state to accepting states
        # Will need to change when functions other than concatenation are supported.
        if assume_accept:
            self.accepting_states = [new_state]  # TODO currently overwrites old

        # Add transition from old_state to new_state
        self.add_to_transition_function((old_state, transition_char), new_state)

        return new_state

    def add_epsilon_connector(self, old_state: State) -> State:
        """
        add_epsilon_connector
        Add necessary states and transitions to connect one state to a new one on epsilon.
        Invariants: state is in self.states. New state will not be accepting.

        :param old_state: The state to transition from.
        :return: The state representing the final state of this sequence.
        """

        return self.add_normal_char(old_state, EPSILON, False)

    def replace_initial(self) -> State:
        """
        replace_initial
        Build a new initial state and epsilon transition to the old one.

        :return: The new initial state.
        """

        # make a state
        new_state = State(len(self.states))
        self.states.append(new_state)

        # epsilon the state to initial
        self.add_to_transition_function((new_state, EPSILON), self.initial_state)

        # replace initial
        self.initial_state = new_state

        return new_state

    def run_nfa(self, input_string: str) -> bool:
        """
        run_nfa
        Run a string through an NFA.

        :param input_string: The string to run.
        :return: True if string was accepted. False otherwise.
        """

        # set up the current state
        current_state = start_state if start_state else self.initial_state
        if current_state in self.accepting_states:
            return True

        destination_states = self.transition_function[(current_state, EPSILON)]
        resulting_states = []
        for state in destination_states:
            resulting_states += self.run_nfa(input_string, state)



        destination_states = self.transition_function[(current_state, input_string[0])]





        # process while not rejected and not at end of input string
        for index, char in enumerate(input_string):
            # take all epsilon transitions while available
            while (current_state, EPSILON) in self.transition_function:
                destination_states = self.transition_function[(current_state, )]
                accepted = []
                for state in destination_states:
                    accepted += self.run_nfa(input_string[index:], state)
                return True in accepted






            # check if there is a corresponding transition
            if not (current_state, c) in self.transition_function.keys():
                # no corresponding transition, reject
                return False
            # follow the transition
            current_state = self.transition_function[(current_state, c)]
        # if ended in an accept state, accept
        return current_state in self.accepting_states
