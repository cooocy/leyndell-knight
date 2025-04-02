import math
import os.path
import re
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


def find_files_by_regex(regex_path) -> List[str]:
    """
    Find files by regex.
    :param regex_path: e.g. ~/.zcompdump*
    """
    regex_path = os.path.expanduser(regex_path)
    base_dir = get_parent_full_dir(regex_path)
    regex_file_name = regex_path.replace(f'{base_dir}/', '')
    if not os.path.exists(base_dir) or not os.path.isdir(base_dir):
        return []

    try:
        regex = re.compile(regex_file_name)
    except re.error as e:
        print(f"Invalid regular expression: {e}")
        return []

    matching_files = []
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if regex.search(file_path):
            matching_files.append(file_path.__str__())

    return matching_files
