from typing import Optional

from overtake.incompatibility_reasons import IncompatibilityReason


class IncompatibilityTypeHintBasic(IncompatibilityReason):
    """we lazy-load the beartype error message because die_if_unbearable is a lot slower
    than is_bearable."""

    def __init__(self, value: object, type_hint: object, argument_name: str):
        self.value = value
        self.type_hint = type_hint
        self.argument_name = argument_name

    def __str__(self):
        return (
            f"There is a type hint mismatch for argument {self.argument_name}: "
            f"Object {self.value} is of class {self.value.__class__} "
            f"which is not a subclass of {self.type_hint}"
        )


def check_type(
    argument_value: object, type_hint: object, argument_name
) -> Optional[IncompatibilityReason]:
    try:
        if isinstance(argument_value, type_hint):  # type: ignore
            return None
        else:
            return IncompatibilityTypeHintBasic(
                argument_value, type_hint, argument_name
            )
    except TypeError:
        raise TypeError(
            "The basic type checker built-in into overtake cannot handle type-checking"
            f" of {type_hint},you should try with beartype which has support for more"
            " type hints. Run `pip install overtake[beartype]` "
            "and use `@overtake(runtime_type_checker='beartype')`."
        )
