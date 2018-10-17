from enum import Enum
from typing import List


class RegexSpecialChar(Enum):
    CONCATENATION = '·'
    STAR = '*'
    UNION = '|'
    PLUS = '+'
    OPTIONAL = '?'
    GROUP = '()'
    RANGE = '[-]'

    @staticmethod
    def all_regex_special_chars() -> List[str]:
        return [item.value for item in RegexSpecialChar]
