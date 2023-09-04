import inspect
import sys
import typing
from typing import Callable, Dict, Generic, List, Tuple, TypeVar, Union

from beartype.door import die_if_unbearable
import beartype.roar
from typing_extensions import ParamSpec, get_overloads


class CompatibleOverloadNotFoundError(Exception):
    pass


class OverloadsNotFoundError(Exception):
    pass


T = TypeVar("T")
P = ParamSpec("P")


class OvertakenFunctionRegistry(Generic[P, T]):
    def __init__(self, overtaken_function: Callable[P, T]):
        self.overtaken_function = overtaken_function
        self._implementations: Union[List[Tuple[Callable, inspect.Signature]], None] = (
            None
        )

    @property
    def implementations(self) -> List[Tuple[Callable, inspect.Signature]]:
        if self._implementations is None:
            self._implementations = self._find_implementations()
        return self._implementations

    def _find_implementations(self) -> List[Tuple[Callable, inspect.Signature]]:
        overloaded_implementations = list(get_overloads(self.overtaken_function))
        self.raise_if_no_implementations(overloaded_implementations)

        result = []
        for overloaded_implementation in overloaded_implementations:
            result.append(
                (
                    overloaded_implementation,
                    inspect.signature(overloaded_implementation),
                )
            )
        return result

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        incompatibilities = []
        for overloaded_implementation, signature in self.implementations:
            incompatibility = find_incompatibility(args, kwargs, signature)
            if incompatibility is None:
                return overloaded_implementation(*args, **kwargs)
            else:
                incompatibilities.append(
                    explain_incompatibility_for_one_overload(signature, incompatibility)
                )
        else:
            self.raise_full_incompatibility(incompatibilities)

    def raise_full_incompatibility(
        self, incompatibilities: List[str]
    ) -> typing.NoReturn:
        full_message = (
            f"No compatible overload found for function '{self.overtaken_function}', "
            "here is why: "
        )
        for incompatibility in incompatibilities:
            full_message += "\n"
            full_message += incompatibility
        raise CompatibleOverloadNotFoundError(full_message)

    def raise_if_no_implementations(self, implementations: List[Callable]) -> None:
        if implementations != []:
            return

        if sys.version_info < (3, 11):
            additional_help = (
                "Did you use 'from typing import overload'? If this is the case, use"
                " 'from typing_extensions import overload' instead. \nOvertake cannot"
                " find the @overload from typing before Python 3.11.When you upgrade to"
                " Python 3.11, you'll be able to use 'from typing import overload'."
            )
        else:
            additional_help = "Did you forget to use '@overload'?"
        raise OverloadsNotFoundError(
            "Overtake could not find the overloads for the function"
            f" {self.overtaken_function}. "
            + additional_help
        )


def explain_incompatibility_for_one_overload(
    signature: inspect.Signature, reason: str
) -> str:
    return f"Incompatible with '{signature}' because {reason}"


def find_incompatibility(
    args: Tuple[object, ...], kwargs: Dict[str, object], signature: inspect.Signature
) -> Union[str, None]:
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
            return (
                f"There is a type hint mismatch for argument {argument_name}: " + str(e)
            )

    return None
