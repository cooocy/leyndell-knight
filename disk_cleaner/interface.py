import os
import time

from colorama import Fore, Style
from config import disk_cleaner_cfs
from disk_cleaner import disk_cleaner


def ordinary_clean():
    print('[disk_cleaner] Will do ordinary clean ...')
    time.sleep(1)
    print()
    garbage_names = disk_cleaner_cfs['ordinary']['garbage']
    __do_clean(garbage_names)
    print()
    print('[disk_cleaner] End.')
    print()


def deep_clean():
    print('[disk_cleaner] Will do deep clean ...')
    time.sleep(1)
    print()
    print('[disk_cleaner] End.')
    print()

    # The deep clean including the ordinary clean.
    garbage_names = disk_cleaner_cfs['ordinary']['garbage'] + disk_cleaner_cfs['deep']['garbage']
    __do_clean(garbage_names)
    print()
    print('[disk_cleaner] End.')
    print()


def __do_clean(garbage_names: list[str]):
    scan_result = disk_cleaner.scan_garbage(garbage_names)
    if scan_result.dirs:
        print(
            f'{Fore.RED}[disk_cleaner] The directories can not be cleaned, please modify the yaml.')
        dirs = os.linesep.join(scan_result.dirs)
        print(f'{dirs}{Style.RESET_ALL}')
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
