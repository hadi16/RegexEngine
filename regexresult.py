from typing import Dict, List


class RegexResult:
    def __init__(self, regular_expression: str, test_strings: List[str]):
        self.regular_expression = regular_expression
        self.test_strings_in_language: Dict[str, bool] = {
            test_string: None for test_string in test_strings
        }
