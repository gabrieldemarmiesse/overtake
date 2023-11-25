from abc import ABC, abstractmethod
from inspect import Signature
from typing import Callable, List

from overtake.display_objects import get_fully_qualified_name


class IncompatibilityReason(ABC):
    """We lazy-load all incompatibility reasons to make sure we are as fast as possible,
    It's also a way to keep all error messages in the same file."""

    @abstractmethod
    def __str__(self):
        return super().__str__()


class IncompatibilityBind(IncompatibilityReason):
    def __init__(self, exception: TypeError):
        self.exception = exception

    def __str__(self):
        return str(self.exception)


class IncompatibilityOverload(IncompatibilityReason):
    def __init__(
        self, signature: Signature, signature_incompatibility: IncompatibilityReason
    ):
        self.signature = signature
        self.signature_incompatibility = signature_incompatibility

    def __str__(self):
        return (
            f"Incompatible with '{self.signature}' because"
            f" {self.signature_incompatibility}"
        )


class FullIncompatibilityReason(IncompatibilityReason):
    def __init__(
        self,
        overtaken_function: Callable,
        signatures_incompatibilities: List[IncompatibilityOverload],
    ):
        self.overtaken_function = overtaken_function
        self.signatures_incompatibilities = signatures_incompatibilities

    def __str__(self):
        full_message = (
            "No compatible overload found for function "
            f"'{get_fully_qualified_name(self.overtaken_function)}', "
            "here is why:"
        )
        for incompatibility in self.signatures_incompatibilities:
            full_message += "\n"
            full_message += str(incompatibility)
        return full_message
