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
        self.union_in_progress: List[(State, State)] = []
        self.last_star: List[State] = []

    def transform_to_nfa(self, regex: str) -> NFA:
        """
        transform_to_nfa
        Main entry point to convert regex to NFA by parsing through the regex.

        :param regex: The regular expression to convert.
        :return: An equivalent NFA.
        """

        if not regex:
            print('Empty regex error')
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
        for char in regex:
            # Check if it is a group
            if char in RegexChar.opening_groups():
                self.open_groups.append(self.last_state)  # TODO : test not causing errors
            elif char in RegexChar.closing_groups():
                # close the group
                self.last_closed_group = self.open_groups[-1]
                if self.union_in_progress and self.union_in_progress[-1][0] == self.open_groups[-1]:
                    self.close_union(nfa)
                self.open_groups = self.open_groups[:-1]
            # check if the char is an operator
            elif char in RegexChar.operators():
                if char == RegexChar.UNION.value:
                    self.union_nfa(nfa)
                # apply the operator to the last closed group
                elif self.last_closed_group is None:
                    # Error in regex
                    print('Error applying operator: ', char)
                    return
                else:
                    if char == RegexChar.STAR.value:
                        self.star_nfa(nfa)
                    elif char == RegexChar.OPTIONAL.value:
                        self.option_nfa(nfa)
                    elif char == RegexChar.PLUS.value:
                        self.plus_nfa(nfa)
            # build the state
            elif char.isalnum():
                # if alphanumeric, concatenate
                nfa = self.concatenate_nfa(nfa, char)
            else:
                # error
                print('Error reading character')
                return

        # post processing
        self.last_closed_group = self.open_groups[-1]
        if self.union_in_progress and self.union_in_progress[-1][0] == self.open_groups[-1]:
            self.close_union(nfa)
        self.open_groups = self.open_groups[:-1]
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
        if self.union_in_progress:
            self.last_state = nfa.add_normal_char(
                self.last_state, char_to_concatenate, True, self.union_in_progress[-1][1]
            )
        elif self.last_star:
            self.last_state = nfa.add_normal_char(
                self.last_state, char_to_concatenate, True, self.last_star[-1]
            )
            self.last_star = self.last_star[:-1]
        else:
            self.last_state = nfa.add_normal_char(
                self.last_state, char_to_concatenate, True, self.open_groups[-1]
            )

        return nfa

    def union_nfa(self, nfa: NFA, unioning_state: State = None) -> None:
        """
        union_nfa
        Add a union from the last open group (or initial state) to existing NFA.

        :param nfa: The existing NFA.
        :param unioning_state: An optional state to union from (otherwise: last open group)
        """
        start_union = unioning_state if unioning_state else self.open_groups[-1]

        self.union_in_progress.append((start_union, self.last_state))

        if start_union in nfa.accepting_states:
            nfa.accepting_states.remove(start_union)

        # if my open group is at the initial state, make a new state
        if start_union == nfa.initial_state:
            self.last_state = nfa.replace_initial()
        # otherwise, connect a new epsilon path out of the open group state for the
        # other part of the union
        else:
            self.last_state = nfa.add_epsilon_connector(start_union)

    def close_union(self, nfa: NFA) -> None:
        """
        close_union
        Close the last open union by connecting the two halves (from
        self.union_in_progress and self.last_state) to a new state via epsilon
        """

        # connect last state of each branch
        self.last_state = nfa.close_branch(self.last_state, self.union_in_progress[-1][1])
        self.union_in_progress = self.union_in_progress[:-1]

    def star_nfa(self, nfa: NFA) -> None:
        """
        star_nfa
        Add a star from the last closed group to existing NFA.

        :param nfa: The existing NFA.
        """
        # add star between last closed group and last state
        self.last_state = nfa.add_star(self.last_closed_group, self.last_state)

        # register this as a star
        self.last_star.append(self.last_closed_group)

        # null out the last closed group so it can't be operated on again
        self.last_closed_group = None

    def option_nfa(self, nfa: NFA) -> None:
        """
        option_nfa
        Add an optional group of chars (last closed group) to an NFA

        :param nfa: The existing NFA.
        """

        self.union_nfa(nfa, self.last_closed_group)
        self.close_union(nfa)

    def plus_nfa(self, nfa: NFA) -> None:
        """
        plus_nfa
        Add a plus operation on the last closed group of an existing nfa

        :param nfa: The existing NFA.
        """
        # add plus between last closed group and last state
        self.last_state = nfa.add_plus(self.last_closed_group, self.last_state)

        # register this as a star
        self.last_star.append(self.last_closed_group)

        # null out the last closed group so it can't be operated on again
        self.last_closed_group = None
