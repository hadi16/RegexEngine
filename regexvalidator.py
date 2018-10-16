from regexspecialchar import RegexSpecialChar
from typing import Dict, List


class RegexValidator:
    def __init__(self, regular_expression: str):
        pass

    def _remove_whitespace_characters(self, regular_expression: str) -> str:
        return regular_expression.replace(' ', '')

    def _has_illegal_characters(self, regular_expression: str) -> bool:
        for char in regular_expression:
            if char.isalnum() or char in RegexSpecialChar.all_regex_special_chars():
                continue
            else:
                return True
        return False

    def valid_regular_expression(self, regular_expression: str) -> bool:
        REGEX_OPERATORS = [item.value for item in RegexSpecialChar]
        open_and_close_brackets: Dict[str, str] = {
            RegexSpecialChar.GROUP_LHS.value: RegexSpecialChar.GROUP_RHS.value,
            RegexSpecialChar.RANGE_LHS.value: RegexSpecialChar.RANGE_RHS.value
        }
        # Initialize stack with a $
        stack: List[str] = ['$']
        for regex_character in regular_expression:
            if regex_character in open_and_close_brackets.keys():
                stack.append(open_and_close_brackets[regex_character])
            elif regex_character in open_and_close_brackets.values():
                if stack.pop() != regex_character:
                    return False
            # Last element of stack is opening range bracket.
            elif stack[-1] == RegexSpecialChar.RANGE_LHS.value:
                if regex_character.isalnum():
                    stack.append(regex_character)
                else:
                    return False
            elif stack[-1].isalnum():
                if regex_character == RegexSpecialChar.RANGE_CENTER.value:pass

        if stack == ['$']:
            return True
        else:
            return False
