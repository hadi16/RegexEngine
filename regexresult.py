from typing import Dict, List
from transformation import Transform
from nfa import NFA

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

    ##
    #
    # Description: Run the test strings through the regex by converting to an
    # equivalent NFA.
    #
    ##
    def runTests(self):
        # build equivalent NFA
        t = Transform()
        nfa_model = t.transform_to_NFA(self.regular_expression)

        # run tests on NFA
        for test in self.test_strings_in_language.keys():
            print('testing: ', test)
            self.test_strings_in_language[test] = nfa_model.run_NFA(nfa_model, test)
