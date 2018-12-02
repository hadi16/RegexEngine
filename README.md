# RegexEngine
# Authors: Alex Hadi and Chelle Plaisted

RegexEngine is an engine to process regular expressions and accept or reject test strings.

DEPENDENCIES
-Python 3.6.0 or later (required for f-strings)
-'click' (for help with the command line portion of the project):
  - on Windows: pip install click
  - on macOS: pip3 install click
-'rstr' (for help with generating random strings for accept tests):
  - on Windows: pip install rstr
  - on macOS: pip3 install rstr
-'jsonschema' (for help with validating json formatting in batch mode):
  - on Windows: pip install jsonschema
  - on macOS: pip3 install jsonschema

STEPS TO RUN & EXPECTED OUTPUT
1. Clone the project.
2. Navigate to the directory containing the RegexEngine folder (or folder that contains the code).
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
- \_\_main\_\_.py
    This is the main entry point to the program that calls parse_input() to validate parameters and begin parsing as needed.
- commandparser.py
    This handles the program input: validating usage in parse_input and routing the program to regular mode and batch mode as necessary.
- jsonreader.py
    Class JsonReader to read an input json file into a list of RegexResult objects.
- jsonwriter.py
    Class JsonWriter to write a list of RegexResult objects to the file path output_file_path.
- mutuallyexclusiveoption.py
    Class MutuallyExclusiveOption to ensure that the user does not attempt to use multiple modes simultaneously.
- nfa.py
    Class NFA to create, edit, and run an NFA.
- regexchar.py
    Enumeration class RegexChar specifying the kinds of regular expression characters handled by the engine.
- regexresult.py
    Class RegexResult defines the results of regex application to a set of strings. Results are stored in a {string => bool} dictionary.
- state.py
    Class State specifies a node in an NFA.
- testgenerator.py
    Class TestGenerator creates randomly generated positive and negative tests for the engine.
- testreader.py
    Class TestReader reads all the test cases and converts them to RegexResult objects.
- testwriter.py
    Class TestWriter writes all the tests to JSON files using JsonWriter.
- transformation.py
    Class Transformation to transform regular expression into an NFA.
