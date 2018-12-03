import logging
import os

from jsonwriter import JsonWriter
from regexresult import RegexResult
from typing import List, Tuple


class TestWriter:
    """
    TestWriter
    Class to write the tests. Uses JsonWriter.
    """

    def __init__(self):
        """
        __init__
        Creates a new TestWriter & creates the tests directory.
        """
        self.TESTS_DIRECTORY = "tests/"

        # If the directory doesn't exist, create it.
        if not os.path.exists(self.TESTS_DIRECTORY):
            os.makedirs(self.TESTS_DIRECTORY)

    def get_passed_and_failed_tests(self, tests: List[RegexResult],
                                    positive_tests: bool) -> Tuple[List[RegexResult],
                                                                   List[RegexResult]]:
        """
        get_passed_and_failed_tests
        Filters the passed and failed tests from a list of all the tests.

        :param tests: The tests to filter.
        :param positive_tests: True if positive tests are passed (otherwise False).
        :return: A tuple containing the tests: (passed_tests, failed_tests)
        """

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

        # If they are positive tests, passing is tests that return True (and converse for negative).
        if positive_tests:
            return true_tests, false_tests
        else:
            return false_tests, true_tests

    def get_tests_summary(self, passed_tests: List[RegexResult],
                          failed_tests: List[RegexResult]) -> Tuple[int, int]:
        """
        get_tests_summary
        Returns the number of passed and failed tests as (number_passed, number_failed)

        :param passed_tests: The list of passed tests to check.
        :param failed_tests: The list of failed tests to check.
        :return: (number_passed, number_failed)
        """

        number_passed = sum(
            len(test.test_strings_in_language.values()) for test in passed_tests
        )
        number_failed = sum(
            len(test.test_strings_in_language.values()) for test in failed_tests
        )
        return number_passed, number_failed

    def write_tests_summary(self, output_file_path: str,
                            number_passed: int, number_failed: int) -> None:
        """
        write_tests_summary
        Writes the summary for all the passed and failed tests to a text file.

        :param output_file_path: The file path to write to.
        :param number_passed: The number of passed tests.
        :param number_failed: The number of failed tests.
        """

        with open(self.TESTS_DIRECTORY + output_file_path, 'w') as file:
            file.write(f'Tests total: {number_passed+number_failed}\n')
            file.write(f'Tests passed: {number_passed}\n')
            file.write(f'Tests failed: {number_failed}\n')

    def write_positive_tests(self, all_positive_tests: List[RegexResult]) -> None:
        """
        write_positive_tests
        Takes list of all the positive tests, filters them out by passed or failed, and writes them.

        :param all_positive_tests: The list of all the positive tests.
        """

        passed_tests, failed_tests = self.get_passed_and_failed_tests(all_positive_tests, True)

        # Write the tests using JsonWriter.
        json_writer = JsonWriter()
        json_writer.write_json_output_file(
            self.TESTS_DIRECTORY + 'tests_positive_all.json', all_positive_tests
        )
        json_writer.write_json_output_file(
            self.TESTS_DIRECTORY + 'tests_positive_passed.json', passed_tests
        )
        json_writer.write_json_output_file(
            self.TESTS_DIRECTORY + 'tests_positive_failed.json', failed_tests
        )

        # Write the tests summary.
        number_passed, number_failed = self.get_tests_summary(passed_tests, failed_tests)
        self.write_tests_summary('tests_positive_summary.txt', number_passed, number_failed)

        logging.info('Positive tests written to tests directory: ' + str(self.TESTS_DIRECTORY))

    def write_negative_tests(self, all_negative_tests: List[RegexResult]) -> None:
        """
        write_negative_tests
        Takes list of all the negative tests, filters them out by passed or failed, and writes them.

        :param all_negative_tests: The list of all the negative tests.
        """

        passed_tests, failed_tests = self.get_passed_and_failed_tests(all_negative_tests, False)

        # Write the tests using JsonWriter.
        json_writer = JsonWriter()
        json_writer.write_json_output_file(
            self.TESTS_DIRECTORY + 'tests_negative_all.json', all_negative_tests
        )
        json_writer.write_json_output_file(
            self.TESTS_DIRECTORY + 'tests_negative_passed.json', passed_tests
        )
        json_writer.write_json_output_file(
            self.TESTS_DIRECTORY + 'tests_negative_failed.json', failed_tests
        )

        # Write the tests summary.
        number_passed, number_failed = self.get_tests_summary(passed_tests, failed_tests)
        self.write_tests_summary('tests_negative_summary.txt', number_passed, number_failed)

        logging.info('Negative tests written to tests directory: ' + str(self.TESTS_DIRECTORY))
