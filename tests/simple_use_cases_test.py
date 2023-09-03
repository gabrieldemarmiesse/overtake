from overtake import overtake
from typing import overload


def test_one_argument():
    @overload
    def my_function(my_var: int) -> int:
        return my_var + 1

    @overload
    def my_function(my_var: str) -> str:
        return my_var + "dododo"

    @overtake
    def my_function(my_var):
        raise NotImplementedError

    assert my_function("5153") == "5153dododo"
    assert my_function(3) == 4
