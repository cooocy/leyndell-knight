import copy
import os.path
import shutil

from colorama import Fore, Style
from dataclasses import dataclass
from pathlib import Path
from tools import file_tools
from typing import List


@dataclass
class Dir:
    name: str
    children_count: int


@dataclass
class File:
    name: str
    size: str


@dataclass
class ScanResult:
    dirs: list[Dir]
    files: list[File]
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
    __dirs: list[Dir] = []
    __files: list[File] = []
    __not_exist: list[str] = []

    for filename in garbage_names:
        filename = os.path.expanduser(filename)

        if not os.path.exists(filename):
            __not_exist.append(filename)
            continue

        if os.path.isdir(filename):
            __dirs.append(Dir(filename, len(os.listdir(filename))))
            continue

        if os.path.isfile(filename):
            file_size = os.path.getsize(filename)
            file_size = file_tools.human_readable_size(file_size)
            __files.append(File(filename, file_size))
            continue

        print(f'{Fore.RED}[disk_cleaner] Unreachable Code. {filename}{Style.RESET_ALL}')

    # The file_name in __not_exist may contain *, find by *.
    matched_files = []
    for filename in copy.copy(__not_exist):
        if file_tools.is_wildcard_path(filename):
            found_files = file_tools.find_files_by_wildcard_path(filename)
            if len(found_files) > 0:
                matched_files.extend(found_files)
                # Remove it from __not_exist, means it found files.
                __not_exist.remove(filename)

    # These matched_files are also garbage.
    for filename in matched_files:
        file_size = os.path.getsize(filename)
        file_size = file_tools.human_readable_size(file_size)
        __files.append(File(filename, file_size))

    return ScanResult(__dirs, __files, __not_exist)


def clean(dirs: List[Dir], files: List[File]):
    for d in dirs:
        if os.path.exists(d.name):
            shutil.rmtree(Path(d.name))
            print(
                f'{Fore.GREEN}[disk_cleaner] Dir: {d.name}, Children Count: {d.children_count}, Removed.{Style.RESET_ALL}')
        else:
            print(f'[disk_cleaner] {d.name} not exist.')

    for f in files:
        if os.path.exists(f.name):
            os.remove(f.name)
            print(f'{Fore.GREEN}[disk_cleaner] File: {f.name}, Size: {f.size}, Removed.{Style.RESET_ALL}')
        else:
            print(f'[disk_cleaner] {f.name} not exist.')
