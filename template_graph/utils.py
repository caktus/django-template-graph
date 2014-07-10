#!/usr/bin/python

import sys
import re
from os import walk
from functools import partial


EXTEND_RE = re.compile('\{\%\s*extends.+\%\}')
INCLUDE_RE = re.compile('\{\%\s*include.+\%\}')

PATTERNS = [
    INCLUDE_RE, EXTEND_RE
]

def filter_line(patterns, line):
    for pattern in patterns:
        if bool(pattern.search(line)):
            return line
    return None

filter_line_by_patterns = partial(filter_line, PATTERNS)


def path_walker(path):
    for base, _, filenames in walk(path):
        for filename in filenames:
            yield '/'.join((base, filename))


def line_reader(filename):
    try:
        with open(filename) as f:
            for line in f:
                yield line.strip()
    except IOError:
        yield ''


def filter_lines_in_path_by_patterns(path, filters):
    for filename in path_walker(path):
        for line_number, line in enumerate(line_reader(filename)):
            if filter_line_by_patterns(line):
                yield filename, line_number, line


def main(path):
    for filename, line_number, line in filter_lines_in_path_by_patterns(path, PATTERNS):
        relative_filename = filename.replace(path, '')
        path = '/'.join(relative_filename.split('/')[:-1])
        print path, line


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: python utils.py path")
