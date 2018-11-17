import json
from regexresult import RegexResult
from typing import List
import os

##
#
# Description: Class to read an input json file into a list of RegexResult objects.
##
class JsonReader:
    def __init__(self, input_file: str):
        self.regex_input_list = self._read_json_input_file(input_file)

    def _read_json_input_file(self, input_file_path: str) -> List[RegexResult]:
        # return type
        result_list: List[RegexResult] = []

        # read file
        with open(input_file_path, 'r') as json_file:
            json_regex_objects: List[dict] = json.load(json_file)

            # handle errors
            if type(json_regex_objects) is not list:
                raise Exception('Input file {} not in valid format.'.format(input_file_path))

            # loop through json objects
            for json_regex_dict in json_regex_objects:
                # handle errors
                if type(json_regex_dict) is not dict:
                    raise Exception('Input file {} not in valid format'.format(input_file_path))

                if 'regex' not in json_regex_dict or 'strings' not in json_regex_dict:
                    raise Exception('Input file {} not in valid format'.format(input_file_path))

                # grab regular expression
                regular_expression = json_regex_dict['regex']

                # grab list of test strings
                test_strings = json_regex_dict['strings']

                # handle error : incorrect format for test strings
                if type(test_strings) is not list:
                    raise Exception('Input file {} not in valid format'.format(input_file_path))

                # add regex and test strings to result list
                result_list.append(RegexResult(regular_expression, test_strings))

        # return result
        return result_list
