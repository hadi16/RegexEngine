from enum import Enum
from string import printable
from typing import List


class RegexChar(Enum):
    """
    RegexChar
    Enumeration of all possible characters in a regular expression.
    Test strings should only have RegexChar.ALPHANUMERIC characters in it.
    """

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
        """
        operators
        Returns all possible regular expression operators.

        :return: A list of strings (the regular expression operators).
        """
        return [RegexChar.PLUS.value, RegexChar.STAR.value, RegexChar.UNION.value,
                RegexChar.OPTIONAL.value]

    @staticmethod
    def opening_group() -> str:
        """
        opening_group
        Returns the string representing the opening group character.

        :return: The string that is the opening group character.
        """
        return RegexChar.GROUP.value[0]

    @staticmethod
    def closing_group() -> str:
        """
        closing_group
        Returns the string representing the closing group character.

        :return: The string that is the closing group character.
        """
        return RegexChar.GROUP.value[-1]
