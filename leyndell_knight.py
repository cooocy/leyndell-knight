import sys
from colorama import Fore, Style
from disk_cleaner import interface as disk_cleaner_interface
from oss_helper import interface as oss_helper_interface

__handlers = {
    'dc': disk_cleaner_interface.handle,
    'oss': oss_helper_interface.handle,
}

if __name__ == '__main__':
    # lk oss
    # length of (lk oss) is 2
    # so the length of args must >= 2.
    __argv = sys.argv
    if len(__argv) < 2:
        print(f'{Fore.RED}[leyndell_knight] Args Error.{Style.RESET_ALL}')
        exit(1)

    # __handler_name: oss
    __handler_name = __argv[1]
    __sub_args = __argv[2:]
    __handler = __handlers.get(__handler_name, None)
    if __handler is None:
        print(f'{Fore.RED}[leyndell_knight] Unknown Command.{Style.RESET_ALL}')
        exit(1)

    __handler(__sub_args)
