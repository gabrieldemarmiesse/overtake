from functools import wraps
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

from overtake.overtake_class import OvertakenFunctionRegistry

T = TypeVar("T")
P = ParamSpec("P")


def overtake(func: Callable[P, T]) -> Callable[P, T]:
    registry = OvertakenFunctionRegistry(func)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return registry(*args, **kwargs)

    return wrapper
