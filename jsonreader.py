import json
from regexresult import RegexResult
from typing import List


class JsonReader:
    def __init__(self, input_file: str):
        self.regex_input_list = self._read_json_input_file(input_file)

    def _read_json_input_file(self, input_file_path: str) -> List[RegexResult]:
        result_list: List[RegexResult] = []

        with open('r', input_file_path) as json_file:
            json_regex_objects: List[dict] = json.load(json_file)
            if type(json_regex_objects) is not list:
                raise Exception('Input file {} not in valid format.'.format(input_file_path))

            for json_regex_dict in json_regex_objects:
                if type(json_regex_dict) is not dict:
                    raise Exception('Input file {} not in valid format'.format(input_file_path))

                if 'regex' not in json_regex_dict or 'strings' not in json_regex_dict:
                    raise Exception('Input file {} not in valid format'.format(input_file_path))

                regular_expression = json_regex_dict['regex']

                test_strings = json_regex_dict['strings']
                if type(test_strings) is not list:
                    raise Exception('Input file {} not in valid format'.format(input_file_path))

                result_list.append(RegexResult(regular_expression, test_strings))

        return result_list
