#!/usr/bin/env python3
#
# GlobalChem - Common Regex Patterns
#
# -----------------------------------

class CommonRegexPatterns(object):

    def __init__(self):

        self.name = 'common_regex_patterns'

    @staticmethod
    def get_patterns():

        patterns = {
            'mol2': '^@<\w+?>\w+?\n[COMPOUND_ID]\n(.|\n)*?@<TRIPOS>SUBSTRUCTURE\n.*?\n'
        }

        return patterns
