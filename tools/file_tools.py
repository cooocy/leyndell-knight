import math
import os.path
from pathlib import Path
from typing import List


def human_readable_size(size_in_bytes) -> str:
    """
    Convert byte size to a human-readable format (KB, MB, GB, etc.)
    """

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    if size_in_bytes == 0:
        return "0B"
    k = 1024.0
    magnitude = int(math.floor(math.log(size_in_bytes, k)))
    value = size_in_bytes / (k ** magnitude)
    return f"{value:.2f}{units[magnitude]}"


def get_parent_full_dir(path: str) -> str:
    p = Path(path)
    return path.replace(f'/{p.name}', '')


def split_path(path: str) -> tuple[str, str]:
    """
    Split the path into parent dir and file name.

    Args:
        path (str): The path to split. e.g. /Users/foo/x.png

    Returns:
        tuple[str, str]: A tuple of (parent dir, file name). e.g. ('/Users/foo', 'x.png')
    """

    parent = get_parent_full_dir(path)
    file_name = path.replace(f'{parent}/', '')
    return parent, file_name


def is_wildcard_path(path: str) -> bool:
    return '*' in path


def find_files_by_wildcard_path(wildcard_path) -> List[str]:
    """
    Find files by wildcard path. The wildcard_path can only has one * in the last filename.

    Args:
        wildcard_path (str): The wildcard path to search for files, must be abs path. e.g. /home/foo/test/*.png

    Returns:
        List[str]: A list of matching files.
    """

    parent, son = split_path(wildcard_path)
    if not os.path.exists(parent) or not os.path.isdir(parent):
        return []

    # List all files (no dir) in the parent directory, and check if the filename matches the wildcard.
    matching_files = []
    for file in os.listdir(parent):
        this_file = f'{parent}/{file}'
        if os.path.isfile(this_file):
            # *.png
            # abc*.png
            if '*' == son:
                matching_files.append(this_file)
                continue
            # abc*.png
            idx_of_wildcard = son.index('*')
            s1 = son[:idx_of_wildcard]
            s2 = son[idx_of_wildcard + 1:]
            if file.startswith(s1) and file.endswith(s2):
                matching_files.append(this_file)

    return matching_files


def expanduser_and_sort(paths: List[str]) -> List[str]:
    """
    Expand the `~` symbol in each path to the user\'s home directory and return a sorted list of unique paths.

    Args:
        paths (List[str]): A list of file or directory paths, potentially containing `~`.

    Returns:
        List[str]: A sorted list of unique paths with `~` expanded.
    """

    l = [os.path.expanduser(path) for path in paths]
    unique_l = list(set(l))
    unique_l.sort()
    return unique_l
