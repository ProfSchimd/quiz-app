def trim_common_prefix(a: str, b: str, ignore_case: bool=False) -> tuple(str, str):
    """Removes from both strings the common prefix ignoring case if
    ignore_case is True. If no common prefix exists, returns the two
    original strings.

    Args:
        a (str): first string
        b (str): first string
        ignore_case (bool, optional): If True, prefix comparison ignores case. Defaults to False.

    Returns:
        tuple(str,str): The trimmed strings.
    """
    x = a.casefold() if ignore_case else a
    y = b.casefold() if ignore_case else b
    i = 0
    while(x[i] == y[i]):
        i += 1
    return (a[i:], b[i:])

def trim_common_suffix(a: str, b: str, ignore_case: bool=False) -> tuple(str, str):
    """Removes from both strings the common suffix ignoring case if
    ignore_case is True. If no common prefix exists, returns the two
    original strings.

    Args:
        a (str): first string
        b (str): first string
        ignore_case (bool, optional): If True, suffix comparison ignores case. Defaults to False.

    Returns:
        tuple(str,str): The trimmed strings.
    """
    (t1, t2) = trim_common_prefix(a[-1::-1], b[-1::-1], ignore_case=ignore_case)
    return (t1[-1::-1], t2[-1::-1])


def string_pair_diff_repr(a: str, b: str):
    """Returns a representation of the two given strings trying to
    highlight only the difference of the second with the first.

    Args:
        a (str): first string
        b (str): second string
    """
    pass
    