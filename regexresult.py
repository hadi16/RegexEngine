from typing import Dict, List


class RegexResult:
    def __init__(self, regular_expression: str, test_strings: List[str]):
        self._regular_expression = regular_expression
        self._test_strings_in_language: Dict[str, bool] = {
            test_string: None for test_string in test_strings
        }

    @property
    def regular_expression(self) -> str:
        return self._regular_expression

    @property
    def test_strings_in_language(self) -> Dict[str, bool]:
        return self._test_strings_in_language

    @test_strings_in_language.setter
    def test_strings_in_language(self, value: Dict[str, bool]):
        self._test_strings_in_language = value
