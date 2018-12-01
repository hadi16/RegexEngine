from regexresult import RegexResult
from typing import Dict, List


class TestReader:
    def read_test_cases(self, tests: Dict[str, List[str]]) -> List[RegexResult]:
        return [
            RegexResult(regex, {
                test_string: None for test_string in test_strings
            })
            for regex, test_strings in tests.items()
        ]
