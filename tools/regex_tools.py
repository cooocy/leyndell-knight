import re


def is_valid_regex(pattern: str) -> bool:
    """
    Determine whether the string is a regular expression.
    """
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
