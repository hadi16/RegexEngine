import json
from jsonschema import validate, ValidationError
from regexresult import RegexResult
from typing import List


class JsonReader:
    """
    JsonReader
    Class to read an input json file into a list of RegexResult objects.
    """

    def __init__(self, input_file: str):
        if self._valid_json_input_file(input_file):
            self.regex_input_list = self._read_json_input_file(input_file)
        else:
            self.regex_input_list = []

    def _valid_json_input_file(self, input_file_path: str) -> bool:
        with open(input_file_path, 'r') as regex_file:
            regex_json: List[dict] = json.load(regex_file)
            with open('batch_input_format.schema.json', 'r') as schema_file:
                input_json_schema = json.load(schema_file)
                try:
                    validate(regex_json, input_json_schema)
                    return True
                except ValidationError as e:
                    print(e)
                    return False

    def _read_json_input_file(self, input_file_path: str) -> List[RegexResult]:
        with open(input_file_path, 'r') as regex_file:
            regex_json: List[dict] = json.load(regex_file)
            return [RegexResult(x['regex'], x['strings']) for x in regex_json]
