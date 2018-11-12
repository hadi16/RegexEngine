from typing import Dict, List

##
# Description: This class defines the results of regex application to a set of strings.
# Results are stored in a {string => bool} dictionary.
#
class RegexResult:
    def __init__(self, regular_expression: str, test_strings: List[str]):
        self.regular_expression = regular_expression
        # initialize the results dictionary as {test_string => None}
        self.test_strings_in_language: Dict[str, bool] = {
            test_string: None for test_string in test_strings
        }
