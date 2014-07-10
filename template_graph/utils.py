import re
from os import walk
from functools import partial

from django.template.loaders.filesystem import Loader as FSLoader
from django.conf import settings


fs_loader = FSLoader()

FILENAME_RE = re.compile("""['\\"](?P<fname>[^'"]+)""")
EXTEND_RE = re.compile('\{\%\s*extends.+\%\}')
INCLUDE_RE = re.compile('\{\%\s*include.+\%\}')

INCLUDE_TAG = 0
EXTEND_TAG = 1

PATTERNS = {
    INCLUDE_TAG: INCLUDE_RE,
    EXTEND_TAG: EXTEND_RE,
}



def filter_line(patterns, line):
    for tag, pattern in patterns.items():
        if bool(pattern.search(line)):
            return tag, line
    return None, None


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


def filter_lines_in_path_by_patterns(path, patterns):
    filter_line_by_patterns = partial(filter_line, patterns)
    for filename in path_walker(path):
        for line_number, line in enumerate(line_reader(filename)):
            tag, line = filter_line_by_patterns(line)
            if line is not None:
                yield filename, line_number, tag, line


def find_target_in_line(line):
    target_search = FILENAME_RE.search(line)
    if target_search is None:
        return ''
    else:
        try:
            return target_search.groups()[0]
        except IndexError:
            return ''


def find_targets(line):
    # TODO: Just uses FSLoader for now. Should also use app directories at least
    target_search = FILENAME_RE.search(line)
    if target_search is None:
        return ()
    else:
        try:
            target_value = target_search.groups()[0]
        except IndexError:
            return ()
        else:
            return fs_loader.get_template_sources(target_value)


def stream_template_assocs(template_dirs, patterns):
    for path in template_dirs:
        filtered_lines = filter_lines_in_path_by_patterns(path, patterns)
        for filename, line_number, tag, line in filtered_lines:
            for target in find_targets(line):
                yield tag, filename, line_number, target


def main():
    for tag, filename, line_number, target in stream_template_assocs(settings.TEMPLATE_DIRS, PATTERNS):
        print filename, 'line:', line_number, tag, target


if __name__ == '__main__':
    main()
