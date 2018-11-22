import json
from regexresult import RegexResult
from typing import List


class JsonWriter:
    """
    JsonWriter
    Class to write a list of RegexResult objects to the file path output_file_path.
    """

    def __init__(self, output_file_path: str, regex_result_list: List[RegexResult]):
        self._output_file_path = output_file_path
        self._regex_result_list = regex_result_list

    def write_to_json_file(self) -> None:
        """
        write_to_json_file
        Write self._regex_result_list to self._output_file_path.
        """

        json_list: List[dict] = [
            {
                "regex": regex_result.regular_expression,
                "strings": regex_result.test_strings_in_language
            }
            for regex_result in self._regex_result_list
        ]

        with open(self._output_file_path, 'w') as file:
            file.write(json.dumps(json_list))
