# coding: utf-8


import re


class Match:
    def __init__(self):
        pattern = self.load_pattern()
        synonym = self.load_synonym()
        self.regex = self.make_regex(pattern, synonym)

    def load_pattern(self):
        pattern = {}
        with open("pattern.txt", 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = line.strip()
                no, patts = line.split(':')
                pattern[no] = patts.split('|')
                line = f.readline()
        return pattern

    def load_synonym(self):
        synonym = {}
        with open("synonym.txt", 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = line.strip()
                no, syno = line.split(':')
                synonym[no] = syno.split(',')
                line = f.readline()
        return synonym

    def make_regex(self, pattern, synonym):
        regex = {}
        for no, patts in pattern.items():
            _regex = ""
            for patt in patts:
                _regex += ".*"
                for syno_no in patt:
                    if syno_no == "-":
                        _regex += ".*"
                    else:
                        _regex += "(" + "|".join(synonym[syno_no]) + ")"
                _regex += ".*|"
            regex[no] = _regex[:-1]
        return regex

    def judge_action(self, message):
        for no, _regex in self.regex.items():
            if re.compile(_regex).search(message):
                return no
        return -1
