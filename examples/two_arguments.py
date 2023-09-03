from overtake import overtake
from typing import overload


@overload
def my_function(my_var: int, my_second: float) -> int:  # type: ignore
    print("THis is int")
    return my_var + 1


@overload
def my_function(my_var: str, my_second: float) -> str:  # type: ignore
    print("this is str")
    return my_var + "dododo"


@overtake
def my_function(my_var, my_second):
    raise NotImplementedError


assert my_function("5153", my_second=5.2) == "5153dododo"

assert my_function(3, my_second=5.2) == 4