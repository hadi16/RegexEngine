import json
from regexresult import RegexResult
from typing import Dict, List


class JsonWriter:
    """
    JsonWriter
    Class to write a list of RegexResult objects to the file path output_file_path.
    """

    def create_json_test_input_file(self, regex_list: Dict[str, List[str]],
                                    input_file_path: str) -> None:
        json_list = [
            {
                "regex": regex,
                "strings": regex_list[regex]
            }
            for regex in regex_list
        ]

        with open(input_file_path, 'w') as file:
            file.write(json.dumps(json_list))

    def write_json_output_file(self, output_file_path: str,
                               regex_result_list: List[RegexResult]) -> None:
        """
        write_json_output_file
        Write self._regex_result_list to self._output_file_path.
        """

        json_list: List[dict] = [
            {
                "regex": regex_result.regular_expression,
                "strings": regex_result.test_strings_in_language
            }
            for regex_result in regex_result_list
        ]

        with open(output_file_path, 'w') as file:
            file.write(json.dumps(json_list))
