from nfa.node import Node
from regexspecialchar import RegexOperator
from typing import Dict, List


class Transformation:
    def _optional(self, nfa: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        pass

    def _plus(self, nfa: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        pass

    def _star(self, nfa: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        pass

    def _union(self, nfa: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        pass

    def perform_regex_operation(self, operator: RegexOperator) -> Dict[str, List[Node]]:
        regex_transformation_operator_func: Dict[RegexOperator, function] = {
            RegexOperator.OPTIONAL:  self._optional,
            RegexOperator.PLUS:      self._plus,
            RegexOperator.STAR:      self._star,
            RegexOperator.UNION:     self._union
        }
        return regex_transformation_operator_func.get(operator)()
