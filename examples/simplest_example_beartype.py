from beartype.vale import Is
from overtake import overtake
from typing_extensions import Annotated, overload

# Type hint matching only strings with lengths ranging [4, 40].
LengthyString = Annotated[str, Is[lambda text: 4 <= len(text) < 40]]

# Type hint matching only strings with lengths ranging [0, 4].
ShortString = Annotated[str, Is[lambda text: 0 <= len(text) < 4]]


@overload
def is_this_string_big(arg: ShortString) -> str:  # type: ignore
    return "This is a short string!"


@overload
def is_this_string_big(arg: LengthyString) -> str:  # type: ignore
    return "This is a very long string"


@overtake(runtime_type_checker="beartype")
def is_this_string_big(arg):  # type: ignore
    ...


print(is_this_string_big("Hi!"))
# This is a short string!
print(is_this_string_big("No one expects the spanish inquisition!"))
# This is a very long string
