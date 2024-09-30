from enum import Enum
import functools


class MergeStrategy(Enum):
    """
    Enum to define different strategies for merging two dictionaries:

    - RAISE: Raises an exception if there's a conflict (i.e., the same key exists in both dictionaries with different values).
    - OVERWRITE: Overwrites the value in the first dictionary with the value from the second dictionary when there's a conflict.
    - IGNORE: Ignores the conflicting value from the second dictionary and keeps the value from the first dictionary.
    - CONCAT_LISTS: If both conflicting values are lists, concatenate them. If they aren't both lists, convert them to lists and concatenate.
    """

    RAISE = "raise"
    OVERWRITE = "overwrite"
    IGNORE = "ignore"
    CONCAT_LISTS = "concat_lists"


def merge(a: dict, b: dict, strategy=MergeStrategy.OVERWRITE, path=[]):
    """
    Merge two dictionaries recursively based on the specified merge strategy.

    Parameters:
    - a (dict): The base dictionary that will be updated.
    - b (dict): The dictionary with new values to merge into `a`.
    - strategy (MergeStrategy): The strategy to handle conflicts (when the same key exists in both `a` and `b`).
      The available strategies are:
        - MergeStrategy.RAISE: Raises an exception when a conflict occurs.
        - MergeStrategy.OVERWRITE: Overwrites the value in `a` with the value from `b`.
        - MergeStrategy.IGNORE: Keeps the value from `a` and ignores the value from `b`.
        - MergeStrategy.CONCAT_LISTS: Concatenates values if both are lists; otherwise, combines them into a list.
    - path (list): Internal use to track the key path during recursion (used for better error messages).

    Returns:
    - dict: The merged dictionary.

    Raises:
    - Exception: If a conflict occurs and the strategy is set to `RAISE`.
    - ValueError: If an unsupported merge strategy is provided.
    """

    for key in b:
        if key in a:
            # If both values are dictionaries, merge them recursively
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], strategy, path + [str(key)])

            # Handle conflict if the values differ and are not both dictionaries
            elif a[key] != b[key]:
                if strategy == MergeStrategy.RAISE:
                    # Raise an exception in case of a conflict
                    raise Exception("Conflict at " + ".".join(path + [str(key)]))

                elif strategy == MergeStrategy.OVERWRITE:
                    # Overwrite the value from `a` with the value from `b`
                    a[key] = b[key]

                elif strategy == MergeStrategy.IGNORE:
                    # Ignore the value from `b` and keep the value in `a`
                    pass

                elif strategy == MergeStrategy.CONCAT_LISTS:
                    # If both values are lists, concatenate them
                    if isinstance(a[key], list) and isinstance(b[key], list):
                        a[key] = a[key] + b[key]
                    # If only one of the values is a list, convert the other value to a list and combine
                    elif isinstance(a[key], list):
                        a[key].append(b[key])
                    elif isinstance(b[key], list):
                        a[key] = [a[key]] + b[key]
                    else:
                        # If neither value is a list, convert both to a list and combine
                        a[key] = [a[key], b[key]]

                else:
                    # Raise an error if an unknown strategy is used
                    raise ValueError(f"Unknown merge strategy: {strategy}")

        else:
            # If the key doesn't exist in `a`, add it from `b`
            a[key] = b[key]

    return a


def merge_old(a: dict, b: dict, path=[]):
    """Merge two dictionaries recursively."""
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] != b[key]:
                raise Exception("Conflict at " + ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def backfill(base: dict, overlay: dict):
    """Deep merge two dictionaries, with the second dictionary taking precedence, back-filling with the first."""
    return merge(base, overlay)


def filternulls(d: dict):
    """Filter out null values from a dictionary, recursively"""

    for k, v in list(d.items()):
        if v is None:
            del d[k]
        elif isinstance(v, dict):
            filternulls(v)
    return d


def non_recursive(decorator):
    @functools.wraps(decorator)
    def wrapper(func):
        # Create an attribute to track recursion state
        func._is_decorating = False

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if func._is_decorating:
                return func(*args, **kwargs)  # Bypass decoration if already decorating

            func._is_decorating = True  # Set recursion flag
            try:
                return decorator(func)(*args, **kwargs)  # Apply decorator
            finally:
                func._is_decorating = False  # Reset flag after execution

        return wrapped_func

    return wrapper
