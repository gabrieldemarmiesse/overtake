from typing import Literal, Optional

from overtake.incompatibility_reasons import IncompatibilityReason
import overtake.runtime_type_checkers.basic
import overtake.runtime_type_checkers.beartype_is_bearable
import overtake.runtime_type_checkers.pydantic_type_adapter

AVAILABLE_TYPE_CHECKERS = Literal["basic", "beartype", "pydantic"]


def check_type(
    argument_value: object,
    type_hint: object,
    argument_name: str,
    runtime_type_checker: AVAILABLE_TYPE_CHECKERS,
) -> Optional[IncompatibilityReason]:
    if runtime_type_checker == "basic":
        return overtake.runtime_type_checkers.basic.check_type(
            argument_value, type_hint, argument_name
        )
    elif runtime_type_checker == "beartype":
        overtake.runtime_type_checkers.beartype_is_bearable.verify_availability()
        return overtake.runtime_type_checkers.beartype_is_bearable.check_type(
            argument_value, type_hint, argument_name
        )
    elif runtime_type_checker == "pydantic":
        overtake.runtime_type_checkers.pydantic_type_adapter.verify_availability()
        return overtake.runtime_type_checkers.pydantic_type_adapter.check_type(
            argument_value, type_hint, argument_name
        )
    else:
        raise ValueError(
            f"Unknown runtime_type_checker. '{runtime_type_checker}' was provided, but"
            " only 'basic' and 'beartype' are available"
        )
