from typing import Literal, Optional

from overtake.incompatibility_reasons import IncompatibilityReason
import overtake.runtime_type_checkers.basic
import overtake.runtime_type_checkers.beartype_is_bearable

AVAILABLE_TYPE_CHECKERS = Literal["basic", "beartype"]


def check_type(
    argument_value: object,
    type_hint: object,
    argument_name: str,
    runtime_type_checker: AVAILABLE_TYPE_CHECKERS,
) -> Optional[IncompatibilityReason]:
    if runtime_type_checker == "basic":
        # Beartype is not installed
        return overtake.runtime_type_checkers.basic.check_type(
            argument_value, type_hint, argument_name
        )
    elif runtime_type_checker == "beartype":
        return overtake.runtime_type_checkers.beartype_is_bearable.check_type(
            argument_value, type_hint, argument_name
        )
    else:
        raise ValueError(
            f"Unknown runtime_type_checker. '{runtime_type_checker}' was provided, but"
            " only 'basic' and 'beartype' are available"
        )
