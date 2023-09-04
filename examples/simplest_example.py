from typing import overload

from overtake import overtake


@overload
def count_words(input_value: list[str]) -> int:  # type: ignore
    total = 0
    for text in input_value:
        total += len(text.split(" "))
    return total


@overload
def count_words(input_value: str) -> int:  # type: ignore
    return len(input_value.split(" "))


@overtake
def count_words(input_value):
    ...


print(count_words(["hello world", "other piece of text"]))
# 6
print(count_words("Python is fun!"))
# 3
