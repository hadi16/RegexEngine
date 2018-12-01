from enum import Enum
from string import printable
from typing import List


class RegexChar(Enum):
    # Operators
    STAR = '*'
    UNION = '|'
    PLUS = '+'
    OPTIONAL = '?'

    # Groups
    GROUP = '()'

    # Valid alphanumeric characters
    ALPHANUMERIC = [x for x in printable if x.isalnum()]

    @staticmethod
    def operators() -> List[str]:
        return [RegexChar.PLUS.value, RegexChar.STAR.value, RegexChar.UNION.value,
                RegexChar.OPTIONAL.value]

    @staticmethod
    def opening_group() -> str:
        return RegexChar.GROUP.value[0]

    @staticmethod
    def closing_group() -> str:
        return RegexChar.GROUP.value[-1]
