import click
import glob
import json
import jsonschema

from regexresult import RegexResult
from typing import List


class JsonReader:
    """
    JsonReader
    Converts an input json file into a list of RegexResult objects.
    """

    def __init__(self, input_file: str):
        """
        __init__
        Creates a JsonReader object.

        :param input_file: The path to the JSON input file.
        """

        # Checks if the JSON file is valid (against a JSON schema).
        if self._valid_json_input_file(input_file):
            self.regex_input_list = self._read_json_input_file(input_file)
        else:
            self.regex_input_list = []

    def _valid_json_input_file(self, input_file_path: str) -> bool:
        """
        _valid_json_input_file
        Checks if the JSON input file is valid (against a JSON schema file).

        :param input_file_path: The path to the input JSON file.
        :return: True if JSON input file is valid (False otherwise).
        """

        # Recursively find the input schema file
        # (deals with different execution points for the program).
        schema_filename = list(glob.iglob('**/batch_input_format.schema.json', recursive=True))[0]
        with open(input_file_path, 'r') as regex_file:
            # Load the input file to validate against.
            regex_json: List[dict] = json.load(regex_file)
            with open(schema_filename, 'r') as schema_file:
                # Load the JSON schema file.
                input_json_schema = json.load(schema_file)

                # Validate the input JSON file against the schema.
                try:
                    jsonschema.validate(regex_json, input_json_schema)
                    return True
                except jsonschema.ValidationError as error_message:
                    click.echo(error_message)
                    return False

    def _read_json_input_file(self, input_file_path: str) -> List[RegexResult]:
        """
        _read_json_input_file
        Reads the JSON input file and converts it to a RegexResult list.

        :param input_file_path:
        :return: A list of RegexResult objects that serve as inputs.
        """

        # Read the input regex file.
        with open(input_file_path, 'r') as regex_file:
            regex_json: List[dict] = json.load(regex_file)

            # Uses list comprehension to return a list of RegexResult objects.
            return [
                RegexResult(x['regex'], {
                    test_string: None for test_string in x['strings']
                })
                for x in regex_json
            ]
