"""This file contains every computation done at the first call of the function."""

import inspect
import sys
from typing import Callable, List, Set, Tuple

from typing_extensions import get_overloads

from overtake.display_objects import get_fully_qualified_name


class OverloadsNotFoundError(Exception):
    pass


class LazyOverloadsInspection:
    def __init__(self, overtaken_function: Callable):
        self.implementations: List[Tuple[Callable, inspect.Signature]] = (
            find_implementations(overtaken_function)
        )
        self.arguments_to_check: Set[str] = _find_arguments_to_check(
            self.implementations
        )


def find_implementations(
    overtaken_function: Callable,
) -> List[Tuple[Callable, inspect.Signature]]:
    overloaded_implementations = list(get_overloads(overtaken_function))
    raise_if_no_implementations(overtaken_function, overloaded_implementations)

    result = []
    for overloaded_implementation in overloaded_implementations:
        result.append(
            (overloaded_implementation, inspect.signature(overloaded_implementation))
        )
    return result


def raise_if_no_implementations(
    overtaken_function: Callable, implementations: List[Callable]
) -> None:
    if implementations != []:
        return

    if sys.version_info < (3, 11):
        additional_help = (
            "Did you use 'from typing import overload'? If this is the case, use"
            " 'from typing_extensions import overload' instead. \nOvertake cannot"
            " find the @overload from typing before Python 3.11. When you upgrade to"
            " Python 3.11, you'll be able to use 'from typing import overload'."
        )
    else:
        additional_help = "Did you forget to use '@overload'?"
    raise OverloadsNotFoundError(
        "Overtake could not find the overloads for the function"
        f" '{get_fully_qualified_name(overtaken_function)}'. "
        + additional_help
    )


def _find_arguments_to_check(
    implementations: List[Tuple[Callable, inspect.Signature]]
) -> Set[str]:
    """We optimise by writing arguments that have types that are changing.

    In some special cases, there might be no types change at all,
    meaning the dispatching is decided by the number of arguments
    provided.
    """
    arguments_to_check = set()
    found_types = {}
    for overloaded_implementation, signature in implementations:
        for argument_name, argument in signature.parameters.items():
            if argument_name not in found_types:
                found_types[argument_name] = argument.annotation
            else:
                if argument.annotation != found_types[argument_name]:
                    # it changed, let's check it later
                    arguments_to_check.add(argument_name)
    return arguments_to_check
