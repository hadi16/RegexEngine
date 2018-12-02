# RegexEngine
# authors: Alex Hadi and Chelle Plaisted

RegexEngine is an engine to process regular expressions and accept or reject test strings.

DEPENDENCIES
-python3
-'click' (for help with the command line portion of the project):
  - on Windows: pip install click
                or to upgrade:
                python -m pip install --upgrade pip
-'rstr' (for help with generating random strings for accept tests):
  - on Windows: pip install rstr
-'jsonschema' (for help with validating json formatting in batch mode):
  - on Windows: pip install jsonschema

STEPS TO RUN & EXPECTED OUTPUT
1. Clone the project.
2. Navigate to the RegexEngine folder.
3. To run in regular mode, enter: "python RegexEngine -r testPattern -s testStr"
  - testPattern : The regular expression you wish to test against.
  - testStr : The string to be checked against the given regular expression.
  - EXPECTED OUTPUT: A line of text output to the terminal structured as follows:
      "'testStr' accepted by regular expression 'testPattern': False"
4. To run in batch mode, enter: "python RegexEngine -i inFile.json -o outFile.json"
  - inFile.json : a json file containing regular expressions and test strings formatting as follows:
  [
    {
      "regex": "a+b",
      "strings": [
          "aab",
          "abab",
          "aaaaab"
       ]
    },
    {
      "regex": "aab*|a",
      "strings": [
          "aaabbbb",
          "ab"
      ]
    }
  ]
  -outfile.json : an empty json file that will be used to record results (see below).
  -EXPECTED OUTPUT: a corresponding JSON file with the resutls of the regular expression test strings, i.e.: 
   [
    {
      "regex": "a+b",
      "strings": [
          "aab": true,
          "abab": false,
          "aaaaab": true
       ]
    },
    {
      "regex": "aab*|a",
      "strings": [
          "aaabbbb": false,
          "ab": false
      ]
    }
  ]
  -NOTE: the file path from the present working directory is needed for the in and output files
5. If there is a usage error running the engine, the user will see an error message i.e.:
  "Usage: RegexEngine [OPTIONS]

  Error: Illegal usage: must provide two command line arguments."
  
  OR
  
  Error reading character
  Error transforming the NFA!
  'testString' accepted by regular expression 'testPattern': None
  
6. Additional flags and options:
  Options:
  -i, --input-file PATH         JSON input file for batch mode. NOTE: This
                                argument is mutually exclusive with
                                arguments: [test-string, regex, generate-
                                tests].
  -o, --output-file PATH        JSON output file for batch mode. NOTE: This
                                argument is mutually exclusive with
                                arguments: [test-string, regex, generate-
                                tests].
  -r, --regex TEXT              Input regular expression for regular mode.
                                NOTE: This argument is mutually exclusive with
                                arguments: [input-file, generate-tests,
                                output-file].
  -s, --test-string TEXT        Input test string for regular mode. NOTE: This
                                argument is mutually exclusive with
                                arguments: [input-file, generate-tests,
                                output-file].
  -t, --generate-tests INTEGER  Create randomly generated tests for the
                                program. Number specified sets the amount of
                                random regular expressions to generate. NOTE:
                                This argument is mutually exclusive with
                                arguments: [input-file, regex, output-file,
                                test-string].
  -v, --verbose                 Enable or disable verbose messages to
                                terminal. Defaults to False.
  --help                        Show this message and exit.

SUPPORTED ELEMENTS
- A|B Union
- AB Concatenation
- A* Star (0 or more copies concatenated together)
- A+ Plus (1 or more copies concatenated together)
- A? Optional (0 or 1 copies of A)

COMPONENT FILES & PURPOSE
- __main__.py
    This is the main entry point to the program that calls parse_input() to validate parameters and begin parsing as needed.
- commandparser.py
    This handles the program input: valdiating usage in parse_input and routing the program to regular mode and batch mode as necessary.
- jsonreader.py
    Class to read an input json file into a list of RegexResult objects.
- jsonwriter.py
    Class to write a list of RegexResult objects to the file path output_file_path.
- mutuallyexclusiveoption.py
    Class to help process command line option dependencies correctly.
- nfa.py
    Class to create, edit, and run an NFA.
- node.py
    Class specifying a node in an NFA.
- regexchar.py
    Class specifying the kinds of regular expression characters handled by the endgine.
- regexresult.py
    This class defines the results of regex application to a set of strings. Results are stored in a {string => bool} dictionary.
- transformation.py
    Class to transform regular expression into an NFA.
