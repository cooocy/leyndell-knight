from oss_helper import command
from typing import List


def handle(args: List[str]):
    __handler = command.get_handler(args[0])
    __handler(args[1:])
