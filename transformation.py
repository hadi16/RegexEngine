from nfa import NFA
from regexchar import RegexChar
from state import State
from typing import List


class Transform:
    """
    Transform
    Class to transform a regular expression into an equivalent NFA.
    """

    def __init__(self):
        self.last_state: State = None
        self.open_groups: List[State] = []
        self.last_closed_group: State = None

    def transform_to_nfa(self, regex: str) -> NFA:
        """
        transform_to_nfa
        Main entry point to convert regex to NFA by parsing through the regex.

        :param regex: The regular expression to convert.
        :return: An equivalent NFA.
        """

        if regex is None:
            return

        # Make an NFA and initialize_nfa
        nfa = NFA()
        nfa.initialize_nfa(regex)
        self.last_state = nfa.initial_state
        self.open_groups.append(self.last_state)

        # Parse regex:
        # If I read an open grouping char (i.e. '(' or '['), add it as an open group.
        # If I read a closed grouping char (i.e. ')' or ']'), move the last open state to closed.
        # If I read an operator, apply the operator to the last closed group.
        # If there are no closed groups, there is an error.
        # If I read a character, process it and set it as the last closed group.
        for c in regex:
            # Check if it is a group
            if c in RegexChar.opening_groups():
                self.open_groups.append(self.last_state)  # TODO : test not causing errors
            elif c in RegexChar.closing_groups():
                # close the group
                self.last_closed_group = self.open_groups[-1]
            # check if it is an operator
            elif c in RegexChar.operators():
                if c == RegexChar.UNION.value:
                    self.union_nfa(nfa)

                # apply the operator to the last closed group
                if self.last_closed_group is None:
                    # Error in regex
                    print('Operator Error!')
                    return
                else:
                    # apply
                    pass  # TODO
            # build the state
            else:
                # if alphanumeric, concatenate
                if c.isalnum():
                    nfa = self.concatenate_nfa(nfa, c)
                else:
                    # error
                    print('character error')
                    return
        return nfa

    def concatenate_nfa(self, nfa: NFA, char_to_concatenate: str) -> NFA:
        """
        concatenate_nfa
        Concatenate a regex char to an existing NFA.

        :param nfa: The existing NFA.
        :param char_to_concatenate: Character from regex to concatenate.
        :return: The resulting NFA.
        """
        # As states are added, update the last state to connect from
        # if this isn't the first char of the regex (only a start state), add an epsilon transition.
        if len(nfa.states) > 1:
            self.last_state = nfa.add_epsilon_connector(self.last_state)

        # add the last state as an last close group
        self.last_closed_group = self.last_state

        # Connect to to new state on concat_char
        self.last_state = nfa.add_normal_char(self.last_state, char_to_concatenate, True)

        return nfa

    def union_nfa(self, nfa: NFA) -> None:
        """
        union_nfa
        Add a union from the last open group (or initial state) to existing NFA.

        :param nfa: The existing NFA.
        :return: The resulting NFA.
        """

        # if my open group is at the initial state, make a new state
        if self.open_groups[-1] == nfa.initial_state:
            self.last_state = nfa.replace_initial()
        # otherwise, connect a new epsilon path out of the open group state for the
        # other part of the union
        else:
            self.last_state = nfa.add_epsilon_connector(self.open_groups[-1])
