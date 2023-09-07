from overtake import overtake
from typing_extensions import overload


@overload
def count_words(input_value: list[str]) -> int:  # type: ignore
    return sum(count_words(text) for text in input_value)


@overload
def count_words(input_value: str) -> int:  # type: ignore
    return len(input_value.split())


@overtake
def count_words(input_value):
    ...


print(count_words("Python is fun!"))
# 3
print(count_words(["hello world", "other piece of text"]))
# 6
