from overtake import overtake
from typing_extensions import overload


@overload
def convert_to_int(input_value: list[str]) -> list[int]:  # type: ignore
    return [int(x) for x in input_value]


@overload
def convert_to_int(input_value: str) -> int:  # type: ignore
    return int(input_value)


@overtake
def convert_to_int(input_value):
    ...


print(convert_to_int("88"))
# 88 (an integer)
print(convert_to_int(["88", "42", "84"]))
# [88, 42, 84] (a list of integers)
