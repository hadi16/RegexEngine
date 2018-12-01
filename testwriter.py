from jsonwriter import JsonWriter
from regexresult import RegexResult
from typing import List, Tuple


class TestWriter:
    def get_passed_and_failed_tests(self, tests: List[RegexResult],
                                    positive_tests: bool) -> Tuple[List[RegexResult],
                                                                   List[RegexResult]]:
        true_tests = []
        false_tests = []
        for i, regex_result in enumerate(tests):
            # Checks if all the test strings are True.
            if all(regex_result.test_strings_in_language.values()):
                true_tests.append(regex_result)

            # Checks if all the test strings are False.
            elif not any(regex_result.test_strings_in_language.values()):
                false_tests.append(regex_result)

            # Must be a mixture of passed and failed test cases within a regular expression.
            else:
                true_tests.append(
                    RegexResult(regex_result.regular_expression, {
                        test_string: result
                        for test_string, result in regex_result.test_strings_in_language.items()
                        if result
                    })
                )

                false_tests.append(
                    RegexResult(regex_result.regular_expression, {
                        test_string: result
                        for test_string, result in regex_result.test_strings_in_language.items()
                        if not result
                    })
                )

        if positive_tests:
            return true_tests, false_tests
        else:
            return false_tests, true_tests

    def write_positive_tests(self, all_positive_tests: List[RegexResult]) -> None:
        passed_tests, failed_tests = self.get_passed_and_failed_tests(all_positive_tests, True)

        json_writer = JsonWriter()
        json_writer.write_json_output_file('tests_positive_all.json', all_positive_tests)
        json_writer.write_json_output_file('tests_positive_passed.json', passed_tests)
        json_writer.write_json_output_file('tests_positive_failed.json', failed_tests)

    def write_negative_tests(self, all_negative_tests: List[RegexResult]) -> None:
        passed_tests, failed_tests = self.get_passed_and_failed_tests(all_negative_tests, False)

        json_writer = JsonWriter()
        json_writer.write_json_output_file('tests_negative_all.json', all_negative_tests)
        json_writer.write_json_output_file('tests_negative_passed.json', passed_tests)
        json_writer.write_json_output_file('tests_negative_failed.json', failed_tests)
