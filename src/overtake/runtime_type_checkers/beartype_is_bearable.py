from typing import Optional

from overtake.incompatibility_reasons import IncompatibilityReason

try:
    import beartype.door
    import beartype.roar
except ImportError:
    beartype = None  # type: ignore


class IncompatibilityTypeHintBeartype(IncompatibilityReason):
    """we lazy-load the beartype error message because die_if_unbearable is a lot slower
    than is_bearable."""

    def __init__(self, value: object, type_hint: object, argument_name: str):
        self.value = value
        self.type_hint = type_hint
        self.argument_name = argument_name

    def __str__(self):
        try:
            beartype.door.die_if_unbearable(self.value, self.type_hint)  # type: ignore
        except beartype.roar.BeartypeDoorHintViolation as e:  # type: ignore
            return (
                f"There is a type hint mismatch for argument {self.argument_name}: "
                + str(e)
            )


def check_type(
    argument_value: object, type_hint: object, argument_name: str
) -> Optional[IncompatibilityReason]:
    if beartype.door.is_bearable(argument_value, type_hint):  # type: ignore
        return None
    else:
        return IncompatibilityTypeHintBeartype(argument_value, type_hint, argument_name)


def verify_availability():
    if beartype is None:
        raise RuntimeError(
            "You have used @overtake(runtime_type_checker='beartype') but beartype"
            " is not installed on your system. Use 'pip install overtake[beartype]'."
        )
