from functools import wraps
from typing import Callable, TypeVar

from typing_extensions import ParamSpec, overload

from overtake.overtake_class import OvertakenFunctionRegistry
from overtake.runtime_type_checkers.umbrella import AVAILABLE_TYPE_CHECKERS

T = TypeVar("T")
P = ParamSpec("P")


@overload
def overtake(func: Callable[P, T], /) -> Callable[P, T]:
    ...


@overload
def overtake(*, runtime_type_checker: AVAILABLE_TYPE_CHECKERS = "basic") -> Callable:
    ...


def overtake(func=None, /, *, runtime_type_checker: AVAILABLE_TYPE_CHECKERS = "basic"):
    if func is None:
        return lambda f: make_registry_and_return_wrapper(
            f, runtime_type_checker=runtime_type_checker
        )

    return make_registry_and_return_wrapper(
        func, runtime_type_checker=runtime_type_checker
    )


def make_registry_and_return_wrapper(
    func: Callable[P, T], *, runtime_type_checker: AVAILABLE_TYPE_CHECKERS = "basic"
) -> Callable[P, T]:
    registry = OvertakenFunctionRegistry(
        func, runtime_type_checker=runtime_type_checker
    )

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return registry(*args, **kwargs)

    return wrapper
