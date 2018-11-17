from enum import Enum
from string import printable
from typing import List


class RegexChar(Enum):
    CONCATENATION = [x for x in printable if x.isalnum()]
    STAR = '*'
    UNION = '|'
    PLUS = '+'
    OPTIONAL = '?'
    GROUP = '()'
    RANGE = '[-]'

    @staticmethod
    def operators() -> List[str]:
        return [RegexChar.PLUS.value, RegexChar.STAR.value, RegexChar.UNION.value,
                RegexChar.OPTIONAL.value]

    @staticmethod
    def opening_groups() -> List[str]:
        return [RegexChar.GROUP.value[0], RegexChar.RANGE.value[0]]

    @staticmethod
    def closing_groups() -> List[str]:
        return [RegexChar.GROUP.value[-1], RegexChar.RANGE.value[-1]]
