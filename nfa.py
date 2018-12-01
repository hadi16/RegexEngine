from state import State
from typing import Dict, List, Tuple
from verboseprint import verbose_print

EPSILON = 'ε'


class NFA:
    """
    NFA
    Class to define the structure of an NFA with helper functions to help build it.
    """

    def __init__(self):
        self.initial_state: State = None
        self.accepting_states: List[State] = []
        self.alphabet: List[str] = []
        self.states: List[State] = []
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
        self.accepting_states.append(initial_state)

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

    def add_normal_char(self, old_state: State, transition_char: str, assume_accept: bool=True,
                        start_path_state: State=None) -> State:
        """
        add_normal_char
        Add necessary states and transitions to connect one state to a new one on some character.
        Invariants: State is in self.states, char is in self.alphabet.
        Assume final state should be an accepting state unless told otherwise.

        :param old_state: The state to transition from.
        :param transition_char: The char to transition on.
        :param assume_accept: Whether to assume final state is accepting or not.
        :param start_path_state: the start of the path of this state.
        :return: The state representing the final state of this sequence.
        """

        # Build a new state to transition to
        new_state = State(len(self.states))

        # Add state to states
        self.states.append(new_state)

        # Add transition from old_state to new_state
        self.add_to_transition_function((old_state, transition_char), new_state)

        # If needed add this to accepting states
        if assume_accept:
            self.clear_accept_from_path(start_path_state, new_state)
            self.accepting_states.append(new_state)

        return new_state

    def clear_accept_from_path(self, start_state: State, end_state: State) -> None:
        """
        clear_accept_from_path

        Clears the accept states on the path of the current end_state from
        self.accepting_states.

        :param start_state: The start state of the path.
        :param end_state: The ending state of the path.
        """

        states_to_delete = range(start_state.state_id, end_state.state_id)
        verbose_print('Deleting accept states in range: ' + str(states_to_delete))
        verbose_print(f'Accepting states: {self.accepting_states}; Length: {len(self.accepting_states)}')
        temporary_states = self.accepting_states.copy()

        for state in self.accepting_states:
            verbose_print('Processing: ' + str(state.state_id))
            if state.state_id in states_to_delete:
                verbose_print('Removing: ' + str(state.state_id))
                temporary_states.remove(state)
        self.accepting_states = temporary_states
        verbose_print('Resulting accepting states: ' + str(self.accepting_states))
        verbose_print('---------')

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

    def close_branch(self, path_end_1: State, path_end_2: State) -> State:
        """
        close_branch

        Build a new state that connects two end states to a new end state
        with epsilon transitions.

        :return: The new final state
        """

        # Makes a new state.
        new_state = State(len(self.states))

        # epsilon transition from end states
        self.add_to_transition_function((path_end_1, EPSILON), new_state)
        self.add_to_transition_function((path_end_2, EPSILON), new_state)

        # alter accept states
        self.accepting_states.append(new_state)
        return new_state

    def add_star(self, start_star: State, end_star: State) -> State:
        """
        add_star

        Connect the start and end with epsilon transitions and edit start states to add star

        :return: The new final state
        """
        self.add_to_transition_function((end_star, EPSILON), start_star)
        new_state = State(len(self.states))
        self.add_to_transition_function((start_star, EPSILON), new_state)

        if not start_star in self.accepting_states:
            self.accepting_states.append(start_star)
        if end_star in self.accepting_states:
            self.accepting_states.remove(end_star)
        self.accepting_states.append(new_state)

        return new_state

    def add_plus(self, start_plus: State, end_plus: State) -> State:
        """
        add_plus

        Connect the start and end with epsilon transitions and edit start states to add plus

        :return: The new final state
        """
        self.add_to_transition_function((end_plus, EPSILON), start_plus)

        if start_plus in self.accepting_states:
            self.accepting_states.remove(start_plus)
        if end_plus not in self.accepting_states:
            self.accepting_states.append(end_plus)

        return end_plus

    def run_nfa(self, input_string: str, current_state: State,
                path: List[Tuple[State, str]]=None) -> bool:
        """
        run_nfa                                  <!-- RECURSIVE -->
        Run a string through an NFA.

        :param input_string: The string to run.
        :param current_state: The state to start from.
        :param path: The path to the current NFA position.
        :return: True if string was accepted. False otherwise.
        """

        if path is None:
            path = []

        path.append((current_state, input_string))

        # Set up the current state
        if current_state in self.accepting_states and input_string is "":
            verbose_print('Accept on path: ' + str(path))
            return True

        # Finds all resulting states from epsilon transitions.
        if (current_state, EPSILON) in self.transition_function:
            destinations = self.transition_function[(current_state, EPSILON)]
            # TODO: Why path.copy() here but not below?
            results = [
                self.run_nfa(input_string, destination, path.copy()) for destination in destinations
            ]
            if True in results:
                verbose_print('accept on path: ', path)
                return True

        # Checks if string has been read through.
        if not input_string:
            verbose_print('reject end str on path: ', path)
            return False

        # Checks if the transition exists in the transition function.
        if (current_state, input_string[0]) in self.transition_function:
            verbose_print(f'Continuing on {current_state} {input_string[0]} to ' +
                          f'{self.transition_function[current_state, input_string[0]]}')

            destinations = self.transition_function[(current_state, input_string[0])]
            verbose_print('Destination: ' + str(destinations))
            results = [
                self.run_nfa(input_string[1:], destination, path) for destination in destinations
            ]
            if True in results:
                verbose_print('Accept on path: ' + str(path))
                return True
        verbose_print('Reject on path is over: ' + str(path))
        return False
