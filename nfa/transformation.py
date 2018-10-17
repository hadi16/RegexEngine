from nfa.node import Node
from regexspecialchar import RegexSpecialChar


class Transformation:
    def _optional(self, nfa: Node) -> Node:
        pass

    def _plus(self, nfa: Node) -> Node:
        pass

    def _star(self, nfa: Node) -> Node:
        pass

    def _union(self, nfa_a: Node, nfa_b: Node) -> Node:
        pass

    def perform_regex_operation(self, operator: RegexSpecialChar, nfa_a: Node, nfa_b: Node=None) -> Node:
        if operator == RegexSpecialChar.OPTIONAL:
            return self._optional(nfa_a)
        elif operator == RegexSpecialChar.PLUS:
            return self._plus(nfa_a)
        elif operator == RegexSpecialChar.STAR:
            return self._star(nfa_a)
        elif operator == RegexSpecialChar.UNION:
            return self._union(nfa_a, nfa_b)
