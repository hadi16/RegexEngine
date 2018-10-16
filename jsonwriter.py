import json
from regexresult import RegexResult
from typing import List


class JsonWriter:
    def __init__(self, output_file_path: str, regex_result_list: List[RegexResult]):
        self._output_file_path = output_file_path
        self._regex_result_list = regex_result_list

    def write_to_json_file(self) -> None:
        json_list: List[dict] = []
        for regex_result in self._regex_result_list:
            json_list.append({
                "regex":    regex_result.regular_expression,
                "strings":  regex_result.test_strings_in_language
            })

        with open('w', self._output_file_path) as file:
            file.write(json.dumps(json_list))
