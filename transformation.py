from nfa import NFA


##
#
# Description: Class to transform a regular expression into an equivalent NFA.
class Transform:
    def __init__(self):
        self.lastState = None

    ##
    # Description: main entry point to convert regex to NFA by parsing through the regex
    #
    # Parameters:
    #   regex: the regular expression to convert.
    #
    # Return: An equivalent NFA.
    ##
    def transform_to_NFA(self, regex: str) -> NFA:
        if regex is None:
            return None

        # build alphabet
        alphabet = set()

        for c in regex:
            # if c in RegexChar.CONCATENATION:
            if c.isalnum():
                alphabet.add(c)
        # make an NFA and initialize
        nfa = NFA()
        nfa.initialize(alphabet)
        self.lastState = nfa.initial_state

        # parse regex
        for c in regex:
            # TODO: only supports concatenation
            # if alphanumeric, concatenate
            if c.isalnum():
                nfa = self._concatenation(nfa, c)
        return nfa

    ##
    # Description: concatenate a regex char to existing NFA.
    #
    # Parameters:
    #   nfa: the existing NFA.
    #   concat_char: character from regex to concatenate.
    #
    # Return: The resulting NFA.
    ##
    def _concatenation(self, nfa: NFA, concat_char: str) -> NFA:
        # As states are added, update the last state to connect from
        # if this isn't the first char of the regex (only a start state), add an epsilon transition.
        if len(nfa.states) > 1:
            self.lastState = nfa.addEpsilonConnector(self.lastState)

        # Connect to to new state on concat_char
        self.lastState = nfa.addNormalChar(self.lastState, concat_char, True)

        return nfa

    # def _concatenation(self, nfa_a: Nfa, nfa_b: Nfa) -> Nfa:
    #     for nfa_a_accepting_node in nfa_a.accepting_nodes:
    #         if '' in nfa_a_accepting_node.transitions:
    #             nfa_a_accepting_node.transitions[''].append(nfa_b.initial_node)
    #         else:
    #             nfa_a_accepting_node.transitions[''] = [nfa_b.initial_node]
    #     return Nfa(nfa_a.initial_node, nfa_b.accepting_nodes)

    # def _optional(self, nfa: Nfa) -> Nfa:
    #     pass
    #
    # def _plus(self, nfa: Nfa) -> Nfa:
    #     return self._union(nfa, self._star(nfa))
    #
    # def _star(self, nfa: Nfa) -> Nfa:
    #     for accepting_node in nfa.accepting_nodes:
    #         if '' in accepting_node.transitions:
    #             accepting_node.transitions[''].append(nfa.initial_node)
    #         else:
    #             accepting_node.transitions[''] = [nfa.initial_node]
    #     new_initial_node = Node({
    #         '': [nfa.initial_node]
    #     })
    #     nfa.accepting_nodes.append(new_initial_node)
    #     return Nfa(new_initial_node, nfa.accepting_nodes)
    #
    # def _union(self, nfa_a: Nfa, nfa_b: Nfa) -> Nfa:
    #     initial_node = Node({
    #         '': [nfa_a.initial_node, nfa_b.initial_node]
    #     })
    #     accepting_nodes = nfa_a.accepting_nodes + nfa_b.accepting_nodes
    #     return Nfa(initial_node, accepting_nodes)
    #
    # def transform_nfa(self, operator: RegexChar, nfa_a: Nfa, nfa_b: Nfa=None) -> Nfa:
    #     if operator == RegexChar.OPTIONAL:
    #         return self._optional(nfa_a)
    #     elif operator == RegexChar.PLUS:
    #         return self._plus(nfa_a)
    #     elif operator == RegexChar.STAR:
    #         return self._star(nfa_a)
    #     elif operator == RegexChar.UNION:
    #         return self._union(nfa_a, nfa_b)
    #     elif operator == RegexChar.CONCATENATION:
    #         return self._concatenation(nfa_a, nfa_b)
