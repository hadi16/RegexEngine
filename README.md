# RegexEngine


RegexEngine is an engine to process regular expressions and approve or reject test strings. This is a working document to describe both 
how to use the engine and working remaining on the project.

DEPENDENCIES
Users must have python3 installed.
Users must have 'click' installed (for help with the command line portion of the project):
  - on Windows: pip install click
                or to upgrade
                python -m pip install --upgrade pip

STEPS TO RUN & EXPECTED OUTPUT
1. Clone the project.
2. Navigate to the RegexEngine folder.
3. To run in regular mode, enter: "python RegexEngine -r testPattern -s testStr"
  - testPattern : The regular expression you wish to test against.
  - testStr : The string to be checked against the given regular expression.
  - EXPECTED OUTPUT: A line of text output to the terminal structured as follows:
      "The string 'testStr' is accepted/not accepted by the regular expression 'testPattern.'"
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
5. If there is a usage error on running the engine, the user will see an error message i.e.:
  "Usage: RegexEngine [OPTIONS]

  Error: Illegal usage: must provide two command line arguments."
  Note that other errors are possible.
  
6.To get more information on usage, enter: "python RegexEngine --help"

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
    ???
- nfa.py
- node.py
- regexchar.py
- regexresult.py
    This class defines the results of regex application to a set of strings. Results are stored in a {string => bool} dictionary.
- transformation.py
