import sys
from typing import List

from overtake import CompatibleOverloadNotFoundError, OverloadsNotFoundError, overtake
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


@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="We want to make sure we don't give wrong hints about the error",
)
def test_regular_typing_overload():
    def my_function(my_var: int) -> int:
        return my_var + 1

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
        " Did you forget to use '@overload'?"
    )


def test_regular_typing_overload():
    from typing_extensions import overload

    @overload
    def my_function(my_var: int) -> int:
        return my_var

    @overload
    def my_function(my_var: int, second_var: float) -> int:
        return my_var

    @overload
    def my_function(my_var: str, second_var: float) -> str:
        return my_var

    @overtake
    def my_function(my_var, second_var=None):
        ...

    with pytest.raises(CompatibleOverloadNotFoundError) as err:
        my_function(438.15, 48.5)
    assert (
        str(err.value)
        == "No compatible overload found for function"
        " 'simple_use_cases_test.test_regular_typing_overload.<locals>.my_function',"
        " here is why:\nIncompatible with '(my_var: int) -> int' because too many"
        " positional arguments\nIncompatible with '(my_var: int, second_var: float)"
        " -> int' because There is a type hint mismatch for argument my_var: Object"
        " 438.15 violates type hint <class 'int'>, as float 438.15 not instance of"
        " int.\nIncompatible with '(my_var: str, second_var: float) -> str' because"
        " There is a type hint mismatch for argument my_var: Object 438.15 violates"
        " type hint <class 'str'>, as float 438.15 not instance of str."
    )
