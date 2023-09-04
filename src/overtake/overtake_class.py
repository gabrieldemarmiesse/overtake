import inspect
import sys
import typing
from typing import Callable, Dict, Generic, List, Set, Tuple, TypeVar, Union

from beartype.door import is_bearable
from typing_extensions import ParamSpec, get_overloads

from overtake.incompatibility_reasons import (
    FullIncompatibilityReason,
    IncompatibilityBind,
    IncompatibilityOverload,
    IncompatibilityReason,
    IncompatibilityTypeHint,
)


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
        self._arguments_to_check: typing.Optional[Set[str]] = None

    @property
    def implementations(self) -> List[Tuple[Callable, inspect.Signature]]:
        if self._implementations is None:
            self._initialize()
        return self._implementations

    @property
    def arguments_to_check(self) -> Set[str]:
        if self._arguments_to_check is None:
            self._initialize()
        return self._arguments_to_check

    def _initialize(self):
        self._implementations = self._find_implementations()
        self._arguments_to_check = self._find_arguments_to_check()
        print(self._arguments_to_check)

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

    def _find_arguments_to_check(self) -> Set[str]:
        """We optimise by writing arguments that have types that are changing.

        In some special cases, there might be no types change at all,
        meaning the dispatching is decided by the number of arguments
        provided.
        """
        arguments_to_check = set()
        found_types = {}
        for overloaded_implementation, signature in self.implementations:
            for argument_name, argument in signature.parameters.items():
                if argument_name not in found_types:
                    found_types[argument_name] = argument.annotation
                else:
                    if argument.annotation != found_types[argument_name]:
                        # it changed, let's check it later
                        arguments_to_check.add(argument_name)
        return arguments_to_check

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        incompatibilities = []
        for overloaded_implementation, signature in self.implementations:
            incompatibility = self.find_incompatibility(args, kwargs, signature)
            if incompatibility is None:
                return overloaded_implementation(*args, **kwargs)
            else:
                incompatibilities.append(
                    IncompatibilityOverload(signature, incompatibility)
                )
        else:
            self.raise_full_incompatibility(incompatibilities)

    def raise_full_incompatibility(
        self, incompatibilities: List[IncompatibilityReason]
    ) -> typing.NoReturn:
        error_message = str(
            FullIncompatibilityReason(self.overtaken_function, incompatibilities)
        )
        raise CompatibleOverloadNotFoundError(error_message)

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

    def find_incompatibility(
        self,
        args: Tuple[object, ...],
        kwargs: Dict[str, object],
        signature: inspect.Signature,
    ) -> Union[IncompatibilityReason, None]:
        try:
            bound_arguments = signature.bind(*args, **kwargs)
        except TypeError as e:
            return IncompatibilityBind(e)

        for argument_name in self.arguments_to_check:
            if argument_name not in bound_arguments.arguments:
                continue
            argument_value = bound_arguments.arguments[argument_name]
            type_hint = signature.parameters[argument_name].annotation
            if type_hint == inspect.Parameter.empty:
                continue

            if is_bearable(argument_value, type_hint):
                continue
            else:
                return IncompatibilityTypeHint(argument_name, argument_value, type_hint)

        return None
