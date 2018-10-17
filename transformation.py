from node import Node
from nfa import Nfa
from regexchar import RegexChar


class Transformation:
    def _concatenation(self, nfa_a: Nfa, nfa_b: Nfa) -> Nfa:
        for nfa_a_accepting_node in nfa_a.accepting_nodes:
            if '' in nfa_a_accepting_node.transitions:
                nfa_a_accepting_node.transitions[''].append(nfa_b.initial_node)
            else:
                nfa_a_accepting_node.transitions[''] = [nfa_b.initial_node]
        return Nfa(nfa_a.initial_node, nfa_b.accepting_nodes)

    def _optional(self, nfa: Nfa) -> Nfa:
        pass

    def _plus(self, nfa: Nfa) -> Nfa:
        return self._union(nfa, self._star(nfa))

    def _star(self, nfa: Nfa) -> Nfa:
        pass

    def _union(self, nfa_a: Nfa, nfa_b: Nfa) -> Nfa:
        initial_node = Node(
            {
                '': [nfa_a.initial_node, nfa_b.initial_node]
            })
        accepting_nodes = nfa_a.accepting_nodes + nfa_b.accepting_nodes
        return Nfa(initial_node, accepting_nodes)

    def transform_nfa(self, operator: RegexChar, nfa_a: Nfa, nfa_b: Nfa=None) -> Nfa:
        if operator == RegexChar.OPTIONAL:
            return self._optional(nfa_a)
        elif operator == RegexChar.PLUS:
            return self._plus(nfa_a)
        elif operator == RegexChar.STAR:
            return self._star(nfa_a)
        elif operator == RegexChar.UNION:
            return self._union(nfa_a, nfa_b)
        elif operator == RegexChar.CONCATENATION:
            return self._concatenation(nfa_a, nfa_b)
