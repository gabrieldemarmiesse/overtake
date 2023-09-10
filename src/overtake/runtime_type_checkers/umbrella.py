from typing import Optional

from overtake.incompatibility_reasons import IncompatibilityReason
import overtake.runtime_type_checkers.basic
import overtake.runtime_type_checkers.beartype_is_bearable


def check_type(
    argument_value: object, type_hint: object, argument_name: str
) -> Optional[IncompatibilityReason]:
    if overtake.runtime_type_checkers.beartype_is_bearable.beartype is None:
        # Beartype is not installed
        return overtake.runtime_type_checkers.basic.check_type(
            argument_value, type_hint, argument_name
        )
    else:
        return overtake.runtime_type_checkers.beartype_is_bearable.check_type(
            argument_value, type_hint, argument_name
        )
