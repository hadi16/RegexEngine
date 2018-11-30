import click

from jsonreader import JsonReader
from jsonwriter import JsonWriter
from mutuallyexclusiveoption import MutuallyExclusiveOption
from regexresult import RegexResult
from testfilegenerator import TestFileGenerator
from typing import Tuple


# Click function decorators to simplify command line processing
@click.command()
@click.option('--input-file', '-i',
              cls=MutuallyExclusiveOption,
              help='JSON input file for batch mode.',
              type=click.Path(exists=True),
              mutually_exclusive=['regex', 'test-string',
                                  'generate-test-input', 'generate-test-output'])
@click.option('--output-file', '-o',
              cls=MutuallyExclusiveOption,
              help='JSON output file for batch mode.',
              type=click.Path(exists=False),
              mutually_exclusive=['regex', 'test-string',
                                  'generate-test-input', 'generate-test-output'])
@click.option('--regex', '-r',
              cls=MutuallyExclusiveOption,
              help='Input regular expression for regular mode.',
              mutually_exclusive=['input-file', 'output-file',
                                  'generate-test-input', 'generate-test-output'])
@click.option('--test-string', '-s',
              cls=MutuallyExclusiveOption,
              help='Input test string for regular mode.',
              mutually_exclusive=['input-file', 'output-file',
                                  'generate-test-input', 'generate-test-output'],
              multiple=True)
@click.option('--generate-tests-input', '-ti',
              cls=MutuallyExclusiveOption,
              help='Input file to create when randomly generating tests for the program.',
              type=click.Path(exists=False),
              mutually_exclusive=['input-file', 'output-file',
                                  'regex', 'test-string'])
@click.option('--generate-tests-output', '-to',
              cls=MutuallyExclusiveOption,
              help='Ouput file to create when randomly generating tests for the program.',
              type=click.Path(exists=False),
              mutually_exclusive=['input-file', 'output-file',
                                  'regex', 'test-string'])
def parse_input(input_file: str, output_file: str, regex: str, test_string: Tuple[str],
                generate_tests_input: str, generate_tests_output: str) -> None:
    """
    parse_input
    Analyze program parameters, report any errors, and route to regular or batch mode as needed.

    :param input_file: optional name of input file. Must be .json if included.
    :param output_file: optional name of output file. Must be .json if included.
    :param regex: optional regex pattern.
    :param test_string: optional test string.
    """

    if generate_tests_input and generate_tests_output:
        if not generate_tests_input.endswith('.json') or not generate_tests_output.endswith('.json'):
            raise click.UsageError('Input file and output file must have JSON extension.')
        generate_tests(generate_tests_input, generate_tests_output)
    # If an input and output files are specified, check for .json file type.
    # Direct to batch mode.
    elif input_file and output_file:
        if not input_file.endswith('.json') or not output_file.endswith('.json'):
            raise click.UsageError('Input file and output file must have JSON extension.')
        batch_mode(input_file, output_file)
    # If regex and test string are provided, direct to regular mode.
    elif regex and test_string:
        regular_mode(regex, test_string)
    elif input_file or output_file:
        raise click.UsageError('Illegal usage: input AND output paths required.')
    elif regex or test_string:
        raise click.UsageError('Illegal usage: regex AND test-string required.')
    elif generate_tests_input or generate_tests_output:
        raise click.UsageError('Illegal usage: must pass input AND output paths to generate tests.')
    else:
        raise click.UsageError('Illegal usage: must provide command line arguments.')


def generate_tests(input_path: str, output_path: str) -> None:
    test_generator = TestFileGenerator()
    regex_test_strings = test_generator.create_random_tests()
    json_writer = JsonWriter()
    json_writer.create_json_test_input_file(regex_test_strings, input_path)
    batch_mode(input_path, output_path)


def regular_mode(regex: str, test_strings: Tuple[str]) -> None:
    """
    regular_mode
    Process regex and test strings in regular mode. Output results to terminal.

    :param regex: The input regex.
    :param test_strings: The input test strings.
    """

    # Build the result of the regular expression
    regex_result = RegexResult(regex, list(test_strings))
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

    # read the input file
    regex_result_list = JsonReader(input_file_path).regex_input_list
    for test in regex_result_list:
        test.run_test_strings()
    # Write results to the output_file_path
    json_writer = JsonWriter()
    json_writer.write_json_output_file(output_file_path, regex_result_list)
