import copy
import os.path
from colorama import Fore, Style
from dataclasses import dataclass
from tools import file_tools


@dataclass
class Garbage:
    name: str
    size: str


@dataclass
class ScanResult:
    garbage: list[Garbage]
    dirs: list[str]
    not_exist: list[str]


def find_invalid_garbage_names(garbage_names: list[str]) -> list[str]:
    """
    Identifies invalid paths in a list of garbage file paths.

    An invalid path is defined as:
    1. The parent directory contains a wildcard (*).
    2. The file name contains more than one wildcard (*).
    3. Not an absolute path

    valid paths e.g.
    - ~/a/b/x.png
    - ~/a/b/c/*.png
    - ~/*.png

    Args:
        garbage_names (list[str]): A list of garbage file paths.

    Returns:
        list[str]: A list of invalid paths.
    """

    invalid_garbage_names = []
    for file_name in garbage_names:
        expanded = os.path.expanduser(file_name)
        # This is not a abs path.
        if not os.path.isabs(expanded):
            invalid_garbage_names.append(file_name)
            continue
        parent, son = file_tools.split_path(expanded)
        # Parent dir can not contain *;
        # and file name can not contain more than one *.
        if '*' in parent or son.count('*') > 1:
            invalid_garbage_names.append(file_name)
            continue
    return invalid_garbage_names


def scan_garbage(garbage_names: list[str]) -> ScanResult:
    __garbage: list[Garbage] = []
    __dirs: list[str] = []
    __not_exist: list[str] = []

    for file_name in garbage_names:
        file_name = os.path.expanduser(file_name)

        if not os.path.exists(file_name):
            __not_exist.append(file_name)
            continue

        if os.path.isdir(file_name):
            __dirs.append(file_name)
            continue

        if os.path.isfile(file_name):
            file_size = os.path.getsize(file_name)
            file_size = file_tools.human_readable_size(file_size)
            __garbage.append(Garbage(file_name, file_size))
            continue
        print(f'{Fore.RED}[disk_cleaner] Unreachable Code. {file_name}{Style.RESET_ALL}')

    # The file_name in __not_exist may contain *, find by *.
    matched_files = []
    for file_name in copy.copy(__not_exist):
        if file_tools.is_wildcard_path(file_name):
            found_files = file_tools.find_files_by_wildcard_path(file_name)
            if len(found_files) > 0:
                matched_files.extend(found_files)
                # Remove it from __not_exist, means it found files.
                __not_exist.remove(file_name)

    # These matched_files are also garbage.
    for file_name in matched_files:
        file_size = os.path.getsize(file_name)
        file_size = file_tools.human_readable_size(file_size)
        __garbage.append(Garbage(file_name, file_size))

    return ScanResult(__garbage, __dirs, __not_exist)


def clean(garbage: list[Garbage]):
    for g in garbage:
        file_name = g.name
        if not os.path.exists(file_name):
            print(f'[disk_cleaner] {file_name} does not exist.')
            continue

        if os.path.isdir(file_name):
            print(f'{Fore.MAGENTA}[disk_cleaner] {file_name} is a directory.{Style.RESET_ALL}')
            continue

        if os.path.isfile(file_name):
            os.remove(file_name)
            print(f'{Fore.GREEN}[disk_cleaner] File: {file_name}, Size: {g.size}, Removed.{Style.RESET_ALL}')
            continue
