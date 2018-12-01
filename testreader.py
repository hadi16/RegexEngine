from regexresult import RegexResult
from typing import Dict, List


class TestReader:
    """
    TestReader
    Class that reads the test cases and converts them to RegexResult objects.
    """

    def read_test_cases(self, tests: Dict[str, List[str]]) -> List[RegexResult]:
        """
        read_test_cases
        Reads the test cases and converts them to a list of RegexResult objects.

        :param tests: The test cases to read.
        :return: The list of RegexResult objects to return.
        """

        return [
            RegexResult(regex, {
                test_string: None for test_string in test_strings
            })
            for regex, test_strings in tests.items()
        ]
