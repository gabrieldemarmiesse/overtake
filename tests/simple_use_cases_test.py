import sys
from typing import List

from overtake import OverloadsNotFoundError, overtake
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
        ...

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
        ...

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
        ...

    assert my_function(my_var="5153", unchanged_var=[]) == "5153dododo"
    assert my_function(my_var=3, unchanged_var=[]) == 4


def test_variable_number_of_arguments():
    @typing_extensions.overload
    def my_function(my_var: int) -> int:
        return my_var + 1

    @typing_extensions.overload
    def my_function(my_var: str, my_second: float = 4.1) -> str:
        return my_var + " new chars"

    @overtake
    def my_function(my_var, my_second=4.1):
        ...

    assert my_function("base", my_second=5.2) == "base new chars"
    assert my_function(3) == 4


def test_variable_number_of_arguments_same_types():
    @typing_extensions.overload
    def my_function(my_var: int) -> int:
        return my_var

    @typing_extensions.overload
    def my_function(my_var: int, my_second: float) -> float:
        return my_var + my_second

    @overtake
    def my_function(my_var, my_second=None):
        ...

    assert isinstance(my_function(3), int)
    assert isinstance(my_function(3, 2.5), float)


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
        ...

    assert my_function("5153") == "5153dododo"
    assert my_function(3) == 4


@pytest.mark.skipif(
    sys.version_info >= (3, 11), reason="typing.overloads supported after 3.11"
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
        ...

    with pytest.raises(OverloadsNotFoundError) as err:
        my_function("dodo")
    assert (
        str(err.value)
        == "Overtake could not find the overloads for the function"
        " 'simple_use_cases_test.test_regular_typing_overload.<locals>.my_function'."
        " Did you use 'from typing import overload'? If this is the case, use 'from"
        " typing_extensions import overload' instead. \nOvertake cannot find the"
        " @overload from typing before Python 3.11. When you upgrade to Python 3.11,"
        " you'll be able to use 'from typing import overload'."
    )
