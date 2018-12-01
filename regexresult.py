from click import echo
from typing import Dict, List
from transformation import Transform
from verboseprint import verbose_print


class RegexResult:
    """
    RegexResult
    This class defines the results of regex application to a set of strings.
    Results are stored in a {string => bool} dictionary.
    """

    def __init__(self, regular_expression: str, test_strings_in_language: Dict[str, bool]):
        self.regular_expression = regular_expression
        self.test_strings_in_language = test_strings_in_language

    def convert_regex_result_to_json(self) -> List[dict]:
        # Return a list of dictionaries that represent the list of objects in the JSON.
        return [
            {
                "regex": self.regular_expression,
                "strings": self.test_strings_in_language
            }
        ]

    def run_test_strings(self) -> None:
        """
        run_test_strings
        Run the test strings through the regex by converting to an equivalent NFA.
        """

        # build equivalent NFA
        nfa = Transform().transform_to_nfa(self.regular_expression)
        if nfa is None:
            echo('Error transforming the NFA!')
            return

        verbose_print('Transitions: ' + str(nfa.transition_function))
        verbose_print('Initial state: ' + str(nfa.initial_state))
        verbose_print('Accepting states: ' + str(nfa.accepting_states))

        # run tests on NFA
        for test_string in self.test_strings_in_language:
            verbose_print('Testing string: ' + str(test_string))
            self.test_strings_in_language[test_string] = nfa.run_nfa(test_string, nfa.initial_state)
