# if you are using Python <3.11, you'll need instead
# from typing_extensions import overload
from overtake import overtake
from typing_extensions import overload


@overload
def count_words(arg: str) -> int:  # type: ignore
    return len(arg.split())


@overload
def count_words(arg: list[str]) -> int:  # type: ignore
    return sum(len(text.split()) for text in arg)


@overtake
def count_words(arg):
    ...


print(count_words("one two three!"))
# 3
print(count_words(["one two", "three four five six"]))
# 6
