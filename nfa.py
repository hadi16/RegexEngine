from typing import List
# constant to define 'epsilon'
EPSILON = 0

# Class to define a state of an NFA, identifiable by an id.
class State:
    def __init__(self, id):
        self.id = id
    def __str__(self):
        return "state " +  str(self.id)
    def __repr__(self):
        return str(self)

# class to define the structure of an NFA with helper functions to help build it.
# NOTE: This class will support nondeterministic EPSILON transitions, but will NOT
# support having multiple transitions on the same char from a given state.
class NFA:
    # def __init__(self, initial_state: Node = None, accepting_states: List[Node] = None):
    def __init__(self):
        self.initial_state = None
        self.accepting_states = []
        self.alphabet = []
        self.states = []
        self.transition_function = {} # structure: {(state, char) => state}

    ##
    # initialize
    #
    # Description: initialize the NFA by adding an initial state and alphabet.
    #
    # Parameters:
    #   Alphabet: the input alphabet for this NFA
    ##
    def initialize(self, alphabet):
        self.alphabet = alphabet
        initial_state = State(len(self.states))
        self.states.append(initial_state)
        self.initial_state = initial_state

    ##
    # addNormalChar
    #
    # Description: Add necessary states and transitions to connect one state to
    # a new one on some character. Invariants: state is in self.states(), char is in
    # self.alphabet. Assume final state should be an accepting state unless told otherwise.
    #
    # Parameters:
    #   old_state : the state to transition from.
    #   transition_char: char to transition on
    #
    # Return : the state representing the final state of this sequence.
    ##
    def addNormalChar(self, old_state, transition_char, assume_accept = True):
        # build a new state to transition to
        new_state = State(len(self.states))
        # add state to states
        self.states.append(new_state)
        # add state to accepting states
        if assume_accept:
            self.accepting_states = [new_state] # TODO currently overwrites old
            # accept states. Will need to change when functions other than concatenation are supported.
        # add transiton from old_state to new_state
        self.transition_function[(old_state, transition_char)] = new_state

        return new_state

    ##
    # addEpsilonConnector
    #
    # Description: Add necessary states and transitions to connect one state to
    # a new one on epsilon. Invariants: state is in self.states(). New state will
    # not be accepting.
    #
    # Parameters:
    #   old_state : the state to transition from.
    #
    # Return : the state representing the final state of this sequence.
    ##
    def addEpsilonConnector(self, old_state):
        return self.addNormalChar(old_state, EPSILON, False)

    ##
    #
    # Description: Run a string through an NFA.
    #
    # Return: True if string was accepted. False otherwise.
    ##
    def run_NFA(self, nfa, str):
        # set up the current state
        current_state = self.initial_state
        # process while not rejected and not at end of input string
        for c in str:
            # take all epsilon transitions while available
            while (current_state, EPSILON) in self.transition_function.keys():
                # take it
                current_state = self.transition_function[(current_state, EPSILON)]

            # check if there is a corresponding transition
            if not (current_state, c) in self.transition_function.keys():
                # no corresponding transition, reject
                return False
            # follow the transition
            current_state = self.transition_function[(current_state, c)]
        # if ended in an accept state, accept
        if current_state in self.accepting_states:
            return True
        else:
            return False
