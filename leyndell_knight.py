import sys
from colorama import Fore, Style
from disk_cleaner import interface as disk_cleaner_interface
from typing import List


def __disk_cleaner_handle(sub_args: List[str]):
    if len(sub_args) != 1:
        print(f'{Fore.RED}[disk_cleaner] Args Error.{Style.RESET_ALL}')
        exit(1)
    arg = sub_args[0]
    if 'ordinary' == arg:
        disk_cleaner_interface.ordinary_clean()
        exit(0)
    if 'deep' == arg:
        disk_cleaner_interface.deep_clean()
        exit(0)
    print(f'{Fore.RED}[disk_cleaner] Args Error. Only ordinary or deep.{Style.RESET_ALL}')
    exit(1)


__handlers = {
    'dc': __disk_cleaner_handle,
}

if __name__ == '__main__':
    __argv = sys.argv
    if len(__argv) < 2:
        print(f'{Fore.RED}[leyndell_knight] Args Error.{Style.RESET_ALL}')
        exit(1)

    __handler_name = __argv[1]
    __sub_args = __argv[2:]
    __handler = __handlers.get(__handler_name, None)
    if __handler is None:
        print(f'{Fore.RED}[leyndell_knight] Unknown Command.{Style.RESET_ALL}')
        exit(1)

    __handler(__sub_args)
