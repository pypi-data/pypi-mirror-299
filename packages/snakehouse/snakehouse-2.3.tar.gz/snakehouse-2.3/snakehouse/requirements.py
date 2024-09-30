import typing as tp
import warnings

from .satella import read_lines, find_files


def find_pyx(directory_path: str) -> tp.List[str]:
    """
    Return all .pyx files found in given directory.

    :param directory_path: directory to look through
    :return: .pyx files found
    """
    warnings.warn('This is deprecated. Use find_all instead', DeprecationWarning)
    return list(find_files(directory_path, '(.*)\\.pyx$', scan_subdirectories=True))


def find_c(directory_path: str) -> tp.List[str]:
    """
    Return all .c files found in given directory.

    :param directory_path: directory to look through
    :return: .c files found
    """
    warnings.warn('This is deprecated. Use find_all instead', DeprecationWarning)
    return list(find_files(directory_path, '(.*)\\.c$', scan_subdirectories=True))


def find_pyx_and_c(directory_path: str) -> tp.List[str]:
    """
    Return a list of all .pyx and .c files found in given directory.

    :param directory_path:
    :return: list of all .pyx and .c files found in given directory
    """
    warnings.warn('This is deprecated. Use find_all instead', DeprecationWarning)
    files = find_pyx(directory_path)
    files.extend(find_c(directory_path))
    return files


def read_requirements_txt(path: str = 'requirements.txt'):
    """
    Read requirements.txt and parse it into a list of packages
    as given by setup(install_required=).

    This means it will read in all lines, discard empty and commented ones,
    and discard all those who are an URL.

    Remember to include your requirements.txt inside your MANIFEST.in!

    :param path: path to requirements.txt. Default is `requirements.txt`.
    :return: list of packages ready to be fed to setup(install_requires=)
    """
    lines = read_lines(path)
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if not line.startswith('#'))
    lines = (line for line in lines if not line.startswith('git+'))
    lines = (line for line in lines if not line.startswith('http'))
    lines = (line for line in lines if line)
    lines = (line for line in lines if not line.startwith('--'))
    lines = (line.replace('--extra-index-url ', '') for line in lines)
    lines = (line.replace('--index-url ', '') for line in lines)
    return list(lines)


def read_dependency_links(path: str = 'requirements.txt') -> tp.List[str]:
    """
    Return arguments that can be passed to setup.py dependency_links
    """
    lines = read_lines(path)
    lines = (line for line in lines if line.startwith('--extra'))
    return list(lines)


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