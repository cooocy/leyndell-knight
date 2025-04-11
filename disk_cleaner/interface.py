import os
import time

from colorama import Fore, Style
from config import disk_cleaner_cfs
from disk_cleaner import disk_cleaner
from typing import List


def handle(sub_args: List[str]):
    if len(sub_args) != 1:
        print(f'{Fore.RED}[disk_cleaner] Args Error.{Style.RESET_ALL}')
        exit(1)
    arg = sub_args[0]
    if 'ordinary' == arg:
        __l1_ordinary_clean()
        exit(0)
    if 'deep' == arg:
        __l1_deep_clean()
        exit(0)
    print(f'{Fore.RED}[disk_cleaner] Args Error. Only ordinary or deep.{Style.RESET_ALL}')
    exit(1)


def __l1_ordinary_clean():
    garbage_names = disk_cleaner_cfs['ordinary']['garbage']
    __l2_check(garbage_names)

    print('[disk_cleaner] Will do ordinary clean ...')
    time.sleep(0.8)
    print()
    __l2_do_clean(garbage_names)
    print()
    print('[disk_cleaner] End.')
    print()


def __l1_deep_clean():
    # The deep clean including the ordinary clean.
    garbage_names = disk_cleaner_cfs['ordinary']['garbage'] + disk_cleaner_cfs['deep']['garbage']
    __l2_check(garbage_names)

    print('[disk_cleaner] Will do deep clean ...')
    time.sleep(0.8)
    print()
    __l2_do_clean(garbage_names)
    print()
    print('[disk_cleaner] End.')
    print()


def __l2_check(garbage_names: list[str]):
    print('[disk_cleaner] Check garbage names ...')
    time.sleep(0.5)

    invalid_garbage_names = disk_cleaner.find_invalid_garbage_names(garbage_names)
    if invalid_garbage_names:
        print(f'{Fore.RED}[disk_cleaner] Check End. Invalid garbage names: {Style.RESET_ALL}')
        print(os.linesep.join(invalid_garbage_names))
        print()
        print('[disk_cleaner] The filename must be an absolute path and can only contain one * in the last filename.')
        print()
        exit(1)
    else:
        print(f'{Fore.GREEN}[disk_cleaner] Check End. All garbage names are valid.{Style.RESET_ALL}')
        print()


def __l2_do_clean(garbage_names: list[str]):
    scan_result = disk_cleaner.scan_garbage(garbage_names)
    if scan_result.dirs:
        print(
            f'{Fore.RED}[disk_cleaner] The directories can not be cleaned, please modify the yaml.{Style.RESET_ALL}')
        dirs = os.linesep.join(scan_result.dirs)
        print(f'{dirs}')
        print()
        exit(1)
    if scan_result.not_exist:
        not_exist = os.linesep.join(scan_result.not_exist)
        print(f'[disk_cleaner] These files not exist, no need to clean.')
        print(f'{not_exist}')
        print()

    if scan_result.garbage:
        print(f'{Fore.CYAN}[disk_cleaner] These files will be cleaned.{Style.RESET_ALL}')
        for g in scan_result.garbage:
            print(f'File: {g.name}, Size: {g.size}')
        print()
        cli_input = input(
            f'{Fore.RED}[disk_cleaner]: Do you want to continue? (y/n): {Style.RESET_ALL}').strip().lower()
        if cli_input == 'y':
            disk_cleaner.clean(scan_result.garbage)
        else:
            print(f'{Fore.GREEN}[disk_cleaner]: Canceled.{Style.RESET_ALL}')
