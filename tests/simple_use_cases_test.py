import sys

from overtake import overtake
import pytest


def test_one_argument():
    from typing_extensions import overload

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
