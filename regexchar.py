from enum import Enum
from typing import List


class RegexChar(Enum):
    CONCATENATION = '·'
    STAR = '*'
    UNION = '|'
    PLUS = '+'
    OPTIONAL = '?'
    GROUP = '()'
    RANGE = '[-]'

    @staticmethod
    def all_regex_chars() -> List[str]:
        return [item.value for item in RegexChar]
