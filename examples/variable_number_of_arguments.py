from overtake import overtake
from typing_extensions import overload


@overload
def my_function(my_var: int) -> int:  # type: ignore
    print("THis is int")
    return my_var + 1


@overload
def my_function(my_var: str, my_second: float = 4.1) -> str:  # type: ignore
    print("this is str")
    return my_var + "dododo"


@overtake
def my_function(my_var, my_second=4.1):
    ...


a = my_function("5153", my_second=5.2)
b = my_function(3)
