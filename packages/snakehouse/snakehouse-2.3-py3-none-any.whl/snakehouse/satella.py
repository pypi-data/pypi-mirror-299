"""
This is a brain-dump from piotrmaslanka/satella's to
cut off the dependency and allow earlier Pythons to use
snakehouse.
"""
import typing as tp
import os
import re


def _has_separator(path: str) -> bool:
    # handle Windows case
    if len(path) == 3:
        if path.endswith(':/') or path.endswith(':\\'):
            return False
    return any(map(lambda x: x in path, os.path.sep))

def _cond_join(prefix: tp.Optional[str], filename: str) -> str:
    """or a conditional os.path.join"""
    if prefix is None:
        return filename
    else:
        return os.path.join(prefix, filename)



def find_files(path: str, wildcard: str = r'(.*)',
               prefix_with: tp.Optional[str] = None,
               scan_subdirectories: bool = True,
               apply_wildcard_to_entire_path: bool = False,
               prefix_with_path: bool = True) -> tp.Iterator[str]:
    """
    Look at given path's files and all subdirectories and return an iterator of
    file names (paths included) that conform to given wildcard.

    Note that wildcard is only applied to the file name if apply_wildcard_to_entire_path
    is False, else the wildcard is applied to entire path (including the application of
    prefix_with!).

    Files will be additionally prefixed with path, but only if prefix_with_path is True

    .. warning:: Note that this will try to match only the start of the path. For a complete match
        remember to put a $ at the end of the string!

    :param path: path to look into.
    :param wildcard: a regular expression to match
    :param prefix_with: an optional path component to prefix before the filename with os.path.join
    :param scan_subdirectories: whether to scan subdirectories
    :param apply_wildcard_to_entire_path: whether to take the entire relative path into account
        when checking wildcard
    :param prefix_with_path: whether to add path to the resulting path
    :return: paths with the files. They will be relative paths, relative to path
    """
    if prefix_with_path:
        prefix_with = _cond_join(prefix_with, path)

    for filename in os.listdir(path):
        if scan_subdirectories and os.path.isdir(os.path.join(path, filename)):
            new_prefix = _cond_join(prefix_with, filename)
            yield from find_files(os.path.join(path, filename), wildcard,
                                  prefix_with=new_prefix,
                                  prefix_with_path=False)
        else:
            if apply_wildcard_to_entire_path:
                fn_path = _cond_join(prefix_with, filename)
            else:
                fn_path = filename
            if re.match(wildcard, fn_path):
                yield _cond_join(prefix_with, filename)

def read_lines(path: str, delete_empty_lines: bool = True,
               encoding: str = 'utf-8') -> tp.List[str]:
    """
    Read lines from a particular file, removing end-of-line characters and optionally
    empty lines. Additionally whitespaces (and end-of-line characters) will be removed
    from both ends of each line.

    :param path: path of file to read
    :param delete_empty_lines: set to False if empty lines are not to be removed
    :param encoding: encoding to read the file with
    :return: each line as a separate entry
    """
    with codecs.open(path, 'r', encoding) as f_in:
        lines = [line.strip() for line in f_in.readlines()]
    if delete_empty_lines:
        lines = [line for line in lines if line]
    return lines

def split(path: str) -> tp.List[str]:
    """
    An exact reverse of os.path.join

    Is is true that

    >>> os.path.join(split(a)) == a
    """
    data = list(os.path.split(path))
    while _has_separator(data[0]):
        data = list(os.path.split(data[0])) + data[1:]
    return data


