from multiprocessing import Pool
import random
from regexchar import RegexChar
import rstr
from typing import Dict, List


class TestFileGenerator:
    def create_random_tests(self) -> Dict[str, List[str]]:
        # Create 5,000 different Regular Expressions randomly
        NUM_REGEX = 5000
        regex_list = [self._generate_random_regex() for _ in range(NUM_REGEX)]

        threading_pool = Pool(6)
        test_strings_list = threading_pool.map(self._generate_positive_tests, regex_list)
        random_tests = dict(zip(regex_list, test_strings_list))

        # Remove empty values (no test strings) in the dictionary.
        return {
            regex: test_strings for regex, test_strings in random_tests.items() if test_strings
        }

    def _generate_positive_tests(self, regex: str) -> List[str]:
        NUM_TEST_STRINGS = 20
        # Set is to remove duplicate test strings.
        test_strings = list({rstr.xeger(regex) for _ in range(NUM_TEST_STRINGS)})
        return [
            test_string for test_string in test_strings
            # Limit length of test strings to prevent max recursion depth from being reached.
            if len(test_string) <= 40
        ]

    def _generate_random_regex(self) -> str:
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
                # TODO: Add back? Get recursion depth errors right now.
                # Random chance (60%) of adding operator after closing group.
                # if random.random() < 0.60:
                #     regex += random.choice(RegexChar.operators())
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
