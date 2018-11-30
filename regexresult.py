from typing import Dict, List
from transformation import Transform


class RegexResult:
    """
    RegexResult
    This class defines the results of regex application to a set of strings.
    Results are stored in a {string => bool} dictionary.
    """

    def __init__(self, regular_expression: str, test_strings: List[str], test_mode: bool=False):
        self.regular_expression = regular_expression
        if test_mode:
            self.test_strings_in_language: Dict[str, bool] = {
                test_string: True for test_string in test_strings
            }
        else:
            # initialize_nfa the results dictionary as {test_string => None}
            self.test_strings_in_language: Dict[str, bool] = {
                test_string: None for test_string in test_strings
            }

    def run_test_strings(self) -> None:
        """
        run_test_strings
        Run the test strings through the regex by converting to an equivalent NFA.
        """

        # build equivalent NFA
        nfa_model = Transform().transform_to_nfa(self.regular_expression)
        if nfa_model is None:
            print('Error transforming the NFA!')
            return

        print(nfa_model.transition_function)
        print(nfa_model.initial_state)
        print(nfa_model.accepting_states)

        # run tests on NFA
        for test_string in self.test_strings_in_language:
            print('Testing: ', test_string)
            self.test_strings_in_language[test_string] = nfa_model.run_nfa(test_string, nfa_model.initial_state)
