from enum import Enum
from typing import List


class RegexChar(Enum):
    CONCATENATION = ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F', '0', '1', '2',
    '3', '4', '5', '6', '7', '8', '9'] # note string.isalnum() may be alternative
    STAR = '*'
    UNION = '|'
    PLUS = '+'
    OPTIONAL = '?'
    GROUP = '()'
    RANGE = '[-]'

    @staticmethod
    def all_regex_chars() -> List[str]:
        return [item.value for item in RegexChar]
