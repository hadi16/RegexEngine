import click
import logging
import sys

from jsonreader import JsonReader
from jsonwriter import JsonWriter
from mutuallyexclusiveoption import MutuallyExclusiveOption
from regexresult import RegexResult
from testgenerator import TestGenerator
from testreader import TestReader
from testwriter import TestWriter
from typing import List, Tuple


# Click function decorators to simplify command line processing
@click.command()
@click.option('--input-file', '-i',
              cls=MutuallyExclusiveOption,
              help='JSON input file for batch mode.',
              type=click.Path(exists=True),
              mutually_exclusive=['regex', 'test-string', 'generate-tests'])
@click.option('--output-file', '-o',
              cls=MutuallyExclusiveOption,
              help='JSON output file for batch mode.',
              type=click.Path(exists=False),
              mutually_exclusive=['regex', 'test-string', 'generate-tests'])
@click.option('--regex', '-r',
              cls=MutuallyExclusiveOption,
              help='Input regular expression for regular mode.',
              mutually_exclusive=['input-file', 'output-file', 'generate-tests'])
@click.option('--test-string', '-s',
              cls=MutuallyExclusiveOption,
              help='Input test string for regular mode.',
              mutually_exclusive=['input-file', 'output-file', 'generate-tests'],
              multiple=True)
@click.option('--generate-tests', '-t',
              cls=MutuallyExclusiveOption,
              help='Create randomly generated tests for the program. '
                   'Number specified sets the amount of random regular expressions to generate.',
              type=int,
              mutually_exclusive=['input-file', 'output-file', 'regex', 'test-string'])
@click.option('--verbose', '-v',
              help='Enable or disable verbose messages to terminal. Defaults to False.',
              is_flag=True,
              default=False)
def parse_input(input_file: str, output_file: str, regex: str, test_string: Tuple[str],
                generate_tests: int, verbose: bool) -> None:
    """
    parse_input
    Analyze program parameters, report any errors, and route to regular or batch mode as needed.

    :param input_file: optional name of input file. Must be .json if included.
    :param output_file: optional name of output file. Must be .json if included.
    :param regex: optional regex pattern.
    :param test_string: optional test string.
    :param generate_tests: Number of tests to generate for the program (otherwise None).
    :param verbose: True to display verbose messages to the terminal (otherwise False).
    """

    # Sets the logging mode based on the verbose flag.
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if verbose else logging.INFO)

    # If tests flag is enabled, generate positive and negative tests.
    if generate_tests:
        test_mode(generate_tests)

    # If an input and output files are specified, check for .json file type.
    # Direct to batch mode.
    elif input_file and output_file:
        if not input_file.endswith('.json') or not output_file.endswith('.json'):
            raise click.UsageError('Input file and output file must have JSON extension.')
        batch_mode(input_file, output_file)

    # If regex and test string are provided, direct to regular mode.
    elif regex and test_string:
        regular_mode(regex, test_string)

    # Error handling statements.
    # Checks for cases when user fails to provide both args for a given option (or no args).
    elif input_file or output_file:
        raise click.UsageError('Illegal usage: input AND output paths required.')
    elif regex or test_string:
        raise click.UsageError('Illegal usage: regex AND test-string required.')
    else:
        raise click.UsageError('Illegal usage: must provide command line arguments.')


def _run_all_test_strings_in_list(regex_result_list: List[RegexResult]) -> None:
    """
    _run_all_test_strings_in_list
    Helper method that runs all of the regular expression & test string pairs
    in a given list of RegexResult objects.

    :param regex_result_list: The list of RegexResult objects to go through.
    """

    # Run the test strings for each regex.
    for regular_expression in regex_result_list:
        regular_expression.run_test_strings()


def test_mode(number_of_regex: int) -> None:
    """
    generate_tests
    In this mode, the program creates an input tests file and executes batch mode on this file.
    """

    # Create the test cases as a dictionary of strings (regex)
    # each mapping to a list of strings (test strings).
    test_generator = TestGenerator()
    positive_tests, negative_tests = test_generator.create_tests(number_of_regex)

    # Convert the tests to lists of RegexResult objects.
    test_reader = TestReader()
    positive_tests = test_reader.read_test_cases(positive_tests)
    negative_tests = test_reader.read_test_cases(negative_tests)

    # Run the test strings for the positive and negative tests.
    _run_all_test_strings_in_list(positive_tests)
    _run_all_test_strings_in_list(negative_tests)

    # Write the positive and negative tests.
    test_writer = TestWriter()
    test_writer.write_positive_tests(positive_tests)
    test_writer.write_negative_tests(negative_tests)


def regular_mode(regex: str, test_strings: Tuple[str]) -> None:
    """
    regular_mode
    Process regex and test strings in regular mode. Output results to terminal.

    :param regex: The input regex.
    :param test_strings: The input test strings.
    """

    # Build the result of the regular expression
    regex_result = RegexResult(regex, {
        test_string: None for test_string in list(test_strings)
    })

    # Process the regex on the test string(s).
    regex_result.run_test_strings()

    # output the result for each test string
    for test_string in test_strings:
        click.echo("'{}' accepted by regular expression '{}': {}"
                   .format(test_string, regex, regex_result.test_strings_in_language[test_string]))


def batch_mode(input_file_path: str, output_file_path: str) -> None:
    """
    batch_mode
    Process regex and test strings in batch mode. Output results to output_file_path.

    :param input_file_path: The input JSON file path.
    :param output_file_path: The output JSON file path.
    """

    # read the input file and get an object representation of it.
    regex_result_list = JsonReader(input_file_path).regex_input_list

    if not regex_result_list:
        logging.critical(f'Batch mode failed: {input_file_path} in improper format.')
        return

    # Run all test strings.
    _run_all_test_strings_in_list(regex_result_list)

    # Write results to the output_file_path
    JsonWriter().write_json_output_file(output_file_path, regex_result_list)

    logging.info('Batch mode completed on input file ' + str(input_file_path) +
                 ' and output file ' + str(output_file_path))
