"""
Other useful functions
"""


def is_float(string: (int | str)) -> bool:
    try:
        float(string)
    except ValueError:
        return False

    return True
