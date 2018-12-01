from json import dumps
from regexresult import RegexResult
from typing import List


class JsonWriter:
    """
    JsonWriter
    Writes a list of RegexResult objects to an output file path (JSON output file).
    """

    def write_json_output_file(self, output_file_path: str,
                               regex_result_list: List[RegexResult]) -> None:
        """
        write_json_output_file
        Writes the list of RegexResult objects to the output path.

        :param output_file_path: The output file path (a JSON file).
        :param regex_result_list: The list of RegexResult objects to write to the file.
        """

        json_list = [
            regex_result.convert_regex_result_to_json()
            for regex_result in regex_result_list
        ]

        # Write the list of dictionaries to the JSON file.
        with open(output_file_path, 'w') as file:
            file.write(dumps(json_list))
