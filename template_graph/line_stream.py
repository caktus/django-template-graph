import re
from os import walk
from os.path import exists as path_exists
from functools import partial
from collections import namedtuple

from django.template.loaders.filesystem import Loader as FSLoader
from django.template.loaders.app_directories import Loader as AppLoader
from django.template.loaders.app_directories import app_template_dirs
from django.conf import settings


def get_template_loaders_dirs():
    loader_configs = settings.TEMPLATE_LOADERS
    dirs = ()
    loaders = []
    if 'django.template.loaders.filesystem.Loader' in loader_configs:
        dirs += settings.TEMPLATE_DIRS
        loaders.append(FSLoader())
    if 'django.template.loaders.app_directories.Loader' in loader_configs:
        dirs += app_template_dirs
        loaders.append(AppLoader())
    return loaders, dirs

TLOADERS, TDIRS = get_template_loaders_dirs()

FILENAME_RE = re.compile("""['\\"](?P<fname>[^'"]+)""")
EXTEND_RE = re.compile('\{\%\s*extends.+\%\}')
INCLUDE_RE = re.compile('\{\%\s*include.+\%\}')

INCLUDE_TAG = 'include'
EXTEND_TAG = 'extends'

PATTERNS = {
    INCLUDE_TAG: INCLUDE_RE,
    EXTEND_TAG: EXTEND_RE,
}

TemplateLine = namedtuple('TemplateLine',
    'source target line_number tag_type path')


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


def find_targets(line):
    # TODO: Just uses FSLoader for now. Should also use app directories at least
    target_search = FILENAME_RE.search(line)
    if target_search is None:
        return None
    else:
        try:
            target_value = target_search.groups()[0]
        except IndexError:
            return None
        for loader in TLOADERS:
            fns = loader.get_template_sources(target_value)
            for fn in fns:
                if path_exists(fn):
                    return fn


def stream_template_assocs(template_dirs, patterns):
    for path in template_dirs:
        filtered_lines = filter_lines_in_path_by_patterns(path, patterns)
        for source, line_number, tag_type, line in filtered_lines:
            target = find_targets(line)
            if target is not None:
                yield TemplateLine(source=source, target=target,
                    tag_type=tag_type, line_number=line_number, path=path)


"""
Top level generator that other modules should import and use directly
"""
get_template_line_stream = partial(
    stream_template_assocs, TDIRS, PATTERNS)


if __name__ == '__main__':
    for data in get_template_line_stream():
        print data
