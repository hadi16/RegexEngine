import constants
from click import echo


'''
Citation: https://stackoverflow.com/questions/5980042/
          how-to-implement-the-verbose-or-v-option-into-a-script
'''
verbose_print = echo if constants.VERBOSE else lambda *a, **k: None
