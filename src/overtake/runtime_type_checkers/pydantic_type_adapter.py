from typing import Optional

from overtake.incompatibility_reasons import IncompatibilityReason

try:
    import pydantic
except ImportError:
    pydantic = None  # type: ignore


class IncompatibilityTypeHintPydantic(IncompatibilityReason):
    def __init__(self, error_message: str, argument_name: str):
        self.error_message = error_message
        self.argument_name = argument_name

    def __str__(self):
        return (
            f"There is a type hint mismatch for argument {self.argument_name}:"
            f" {self.error_message}"
        )


def check_type(
    argument_value: object, type_hint: object, argument_name: str
) -> Optional[IncompatibilityReason]:
    try:
        pydantic.TypeAdapter(type_hint).validate_python(argument_value, strict=True)  # type: ignore
    except pydantic.ValidationError as e:  # type: ignore
        return IncompatibilityTypeHintPydantic(str(e), argument_name)
    return None


def verify_availability():
    if pydantic is None:
        raise RuntimeError(
            "You have used @overtake(runtime_type_checker='pydantic') but pydantic is"
            " not installed on your system. Install overtake with 'pip install"
            " overtake[pydantic]"
        )
