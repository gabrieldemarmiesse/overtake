import sys
from typing import List

from overtake import overtake
import pytest
import typing_extensions


def test_one_argument():
    @typing_extensions.overload
    def my_function(my_var: int) -> int:
        return my_var + 1

    @typing_extensions.overload
    def my_function(my_var: str) -> str:
        return my_var + "dododo"

    @overtake
    def my_function(my_var):
        raise NotImplementedError

    assert my_function("5153") == "5153dododo"
    assert my_function(3) == 4


def test_multiple_arguments():
    @typing_extensions.overload
    def my_function(unchanged_var: List[str], my_var: int) -> int:
        return my_var + 1

    @typing_extensions.overload
    def my_function(unchanged_var: List[str], my_var: str) -> str:
        return my_var + "dododo"

    @overtake
    def my_function(unchanged_var, my_var):
        raise NotImplementedError

    assert my_function([], "5153") == "5153dododo"
    assert my_function([], 3) == 4


def test_keyword_arguments():
    @typing_extensions.overload
    def my_function(unchanged_var: List[str], my_var: int) -> int:
        return my_var + 1

    @typing_extensions.overload
    def my_function(unchanged_var: List[str], my_var: str) -> str:
        return my_var + "dododo"

    @overtake
    def my_function(unchanged_var, my_var):
        raise NotImplementedError

    assert my_function(my_var="5153", unchanged_var=[]) == "5153dododo"
    assert my_function(my_var=3, unchanged_var=[]) == 4


def test_variable_number_of_arguments():
    @typing_extensions.overload
    def my_function(my_var: int) -> int:
        print("THis is int")
        return my_var + 1

    @typing_extensions.overload
    def my_function(my_var: str, my_second: float = 4.1) -> str:
        print("this is str")
        return my_var + " new chars"

    @overtake
    def my_function(my_var, my_second=4.1):
        raise NotImplementedError

    assert my_function("base", my_second=5.2) == "base new chars"
    assert my_function(3) == 4


@pytest.mark.skipif(
    sys.version_info < (3, 11), reason="typing.overload available in 3.11"
)
def test_regular_typing_overload():
    from typing import overload

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
