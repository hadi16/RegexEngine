import random
import re
import rstr

from multiprocessing import Pool
from regexchar import RegexChar
from typing import List, Tuple


class TestGenerator:
    """
    TestGenerator
    Class that creates all the tests for the program.
    """

    def __init__(self):
        """
        __init__
        Creates a new TestGenerator object. Just sets some class-level constants.
        """

        self.NUM_TEST_STRINGS = 20
        self.MAX_TEST_STRING_LENGTH = 50

    def create_tests(self, number_of_regex: int) -> Tuple[dict, dict]:
        """
        create_tests
        Creates the positive and negative tests for the program.
        Returns as a tuple like this: (positive_tests, negative_tests)

        :param number_of_regex: The number of random regular expressions to create for the tests.
        :return: (positive_tests, negative_tests)
        """

        # Create different Regular Expressions randomly
        regex_list = [self._generate_random_regex() for _ in range(number_of_regex)]

        # Multiple processes are spawned to make generating the test strings more efficient.
        threading_pool = Pool(6)
        positive_test_strings = threading_pool.map(self._generate_positive_test_strings, regex_list)
        negative_test_strings = threading_pool.map(self._generate_negative_test_strings, regex_list)

        # The index of the regex_list is mapped to each set of positive or negative test string.
        positive_tests = dict(zip(regex_list, positive_test_strings))
        negative_tests = dict(zip(regex_list, negative_test_strings))

        # Remove empty values (no test strings) in the dictionaries and return.
        return (
            {
                regex: test_strings
                for regex, test_strings in positive_tests.items() if test_strings
            },
            {
                regex: test_strings
                for regex, test_strings in negative_tests.items() if test_strings
            }
        )

    def _generate_positive_test_strings(self, regex: str) -> List[str]:
        """
        _generate_positive_test_strings
        Creates a list of positive test strings (test strings in the regular expression).

        :param regex: The regular expression to create the strings from.
        :return: A list of positive test strings.
        """

        # Set is to remove duplicate test strings.
        # xeger generates random test strings in a regular expression.
        test_strings = list({rstr.xeger(regex) for _ in range(self.NUM_TEST_STRINGS)})
        return [
            test_string for test_string in test_strings
            # Limit length of test strings to prevent max recursion depth from being reached.
            if len(test_string) <= self.MAX_TEST_STRING_LENGTH
        ]

    def _generate_negative_test_strings(self, regex: str) -> List[str]:
        """
        _generate_negative_test_strings
        Creates a list of negative test strings (test strings not in the regular expression).

        :param regex: The regular expression to create the strings from.
        :return: A list of negative test strings.
        """

        # Create a list of the alphanumeric elements in the regular expression.
        alphanumeric_regex_elements = list({
            char for char in regex
            if char in RegexChar.ALPHANUMERIC.value
        })

        # To work for regex that has no alphanumeric characters in it.
        if not alphanumeric_regex_elements:
            alphanumeric_regex_elements = RegexChar.ALPHANUMERIC.value

        test_strings = list({
            ''.join(random.choices(
                alphanumeric_regex_elements, k=random.randint(1, self.MAX_TEST_STRING_LENGTH)
            ))
            for _ in range(self.NUM_TEST_STRINGS)
        })

        return [
            test_string for test_string in test_strings
            if self._verify_test_string_not_in_regex(regex, test_string)
        ]

    def _verify_test_string_not_in_regex(self, regex: str, test_str: str) -> bool:
        """
        _verify_test_string_not_in_regex
        Ensures that the randomly generated regular expression isn't in the regular expression.

        :param regex: The regular expression to test against.
        :param test_str: The test string.
        :return: True if not in the regular expression (otherwise False).
        """

        # Add anchors for the beginning and end of line.
        regex_object = re.compile(rf'^{regex}$')
        return not bool(regex_object.match(test_str))

    def _generate_random_regex(self) -> str:
        """
        _generate_random_regex
        Generates a random regular expression.

        :return: A string representing the randomly generated regular expression.
        """

        regex_length = random.randint(1, 20)

        non_union_operators = list(set(RegexChar.operators()) - set(RegexChar.UNION.value))
        # Start with an alphanumeric character or opening group.
        regex: str = random.choice(RegexChar.ALPHANUMERIC.value + [RegexChar.GROUP.value[0]])
        num_open_groups = 1 if regex == RegexChar.GROUP.value[0] else 0
        for i in range(regex_length - 1):
            # 10% chance of adding an opening group.
            if random.random() < 0.10:
                regex += RegexChar.GROUP.value[0]
                num_open_groups += 1
                continue

            # 20% chance of closing an open group.
            if num_open_groups > 0 and random.random() <= 0.20:
                regex += RegexChar.GROUP.value[-1]
                num_open_groups -= 1
                continue

            if regex[-1] in non_union_operators:
                # If the operator isn't a union, a union can follow it.
                if random.random() < 0.25:
                    regex += RegexChar.UNION.value
                    continue

            if regex[-1] in RegexChar.ALPHANUMERIC.value:
                # Have an 70% probability of choosing another alphanumeric character.
                if random.random() < 0.70:
                    regex += random.choice(RegexChar.ALPHANUMERIC.value)
                else:
                    regex += random.choice(RegexChar.operators())
            else:
                regex += random.choice(RegexChar.ALPHANUMERIC.value)

        for _ in range(num_open_groups):
            regex += RegexChar.GROUP.value[-1]

        # Last character of regex cannot be a union.
        if regex.endswith(RegexChar.UNION.value):
            regex = regex[:-1] + random.choice(RegexChar.ALPHANUMERIC.value)

        return regex
