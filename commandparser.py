import click
from jsonreader import JsonReader
from jsonwriter import JsonWriter
from mutuallyexclusiveoption import MutuallyExclusiveOption
from regexresult import RegexResult
from typing import Tuple


@click.command()
@click.option('--input-file', '-i',
              cls=MutuallyExclusiveOption,
              help='JSON input file for batch mode.',
              type=click.Path(exists=True),
              mutually_exclusive=['regex', 'test-string'])
@click.option('--output-file', '-o',
              cls=MutuallyExclusiveOption,
              help='JSON output file for batch mode.',
              type=click.Path(exists=False),
              mutually_exclusive=['regex', 'test-string'])
@click.option('--regex', '-r',
              cls=MutuallyExclusiveOption,
              help='Input regular expression for regular mode.',
              mutually_exclusive=['input-file', 'output-file'])
@click.option('--test-string', '-s',
              cls=MutuallyExclusiveOption,
              help='Input test string for regular mode.',
              mutually_exclusive=['input-file', 'output-file'],
              multiple=True)
def parse_input(input_file: str, output_file: str, regex: str, test_string: Tuple[str]):
    if input_file and output_file:
        if not input_file.endswith('.json') or not output_file.endswith('.json'):
            raise click.UsageError('Input file and output file must have JSON extension.')
        batch_mode(input_file, output_file)
    elif regex and test_string:
        regular_mode(regex, test_string)
    elif input_file or output_file:
        raise click.UsageError('Illegal usage: input AND output paths required.')
    elif regex or test_string:
        raise click.UsageError('Illegal usage: regex AND test-string required.')
    else:
        raise click.UsageError('Illegal usage: must provide two command line arguments.')


def regular_mode(regex: str, test_strings: Tuple[str]):
    regex_result = RegexResult(regex, list(test_strings))
    # TODO: Add regex transformation.
    for test_string in test_strings:
        click.echo("'{}' accepted by regular expression '{}': {}"
                   .format(test_string, regex, regex_result.test_strings_in_language[test_string]))


def batch_mode(input_file_path: str, output_file_path: str):
    regex_result_list = JsonReader(input_file_path).regex_input_list
    # TODO: Add regex transformation.
    json_writer = JsonWriter(output_file_path, regex_result_list)
    json_writer.write_to_json_file()
