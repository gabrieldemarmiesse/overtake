import typing
import inspect

from typing import get_overloads, Callable, TypeVar, ParamSpec, Generic

import beartype.roar
from beartype.door import die_if_unbearable


class CompatibleOverloadNotFoundError(Exception):
    pass

T = TypeVar('T')
P = ParamSpec('P')


class OvertakenFunctionRegistry(Generic[P, T]):
    def __init__(self, overtaken_function: Callable[P, T]):
        self.overtaken_function = overtaken_function
        self._implementations: list[tuple[Callable, inspect.Signature]] | None = None


    @property
    def implementations(self) -> list[tuple[Callable, inspect.Signature]]:
        if self._implementations is None:
            self._implementations = []
            for overloaded_implementation in get_overloads(self.overtaken_function):
                self._implementations.append((overloaded_implementation, inspect.signature(overloaded_implementation)))
        return self._implementations


    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        incompatiblities = []
        for overloaded_implementation, signature in self.implementations:
            incompatibility = find_incompatibility(args, kwargs, signature)
            if incompatibility is None:
                return overloaded_implementation(*args, **kwargs)
            else:
                incompatiblities.append(
                    explain_incompatibility_for_one_overload(signature, incompatibility)
                )
        else:
            self.raise_full_incompatibility(incompatiblities)

    def raise_full_incompatibility(self, incompatiblities: list[str]) -> typing.NoReturn:
        full_message = (f"No compatible overload found for function {self.overtaken_function}, "
                        f"here is why: ")
        for incompatibility in incompatiblities:
            full_message += "\n"
            full_message += incompatibility
        raise CompatibleOverloadNotFoundError(full_message)


def explain_incompatibility_for_one_overload(signature: inspect.Signature, reason: str) -> str:
    return f"Incompatible with {signature} because {reason}"


def find_incompatibility(
        args: tuple[object, ...],
        kwargs: dict[str, object],
        signature: inspect.Signature
    ) -> str | None:
    try:
        bound_arguments = signature.bind(*args, **kwargs)
    except TypeError as e:
        return str(e)

    for argument_name, argument_value in bound_arguments.arguments.items():
        type_hint = signature.parameters[argument_name].annotation
        if type_hint == inspect.Parameter.empty:
            continue
        try:
            die_if_unbearable(argument_value, type_hint)
        except beartype.roar.BeartypeDoorHintViolation as e:
            return f"There is a type hint mismatch for argument {argument_name}: " + str(e)

    return None


