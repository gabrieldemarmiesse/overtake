from overtake import overtake
from overtake.runtime_type_checkers.umbrella import AVAILABLE_TYPE_CHECKERS
import pytest
import typing_extensions
from typing_extensions import TypedDict, Unpack


@pytest.mark.parametrize("runtime_type_checker", ["beartype", "pydantic"])
def test_args(runtime_type_checker: AVAILABLE_TYPE_CHECKERS):
    @typing_extensions.overload
    def my_function(*args: int) -> int:
        return sum(args)

    @typing_extensions.overload
    def my_function(*args: str) -> str:
        return "".join(args)

    @overtake(runtime_type_checker=runtime_type_checker)
    def my_function(*args) -> str | int:
        ...

    assert my_function("5153", "dododo") == "5153dododo"
    assert my_function(3, 3) == 6


@pytest.mark.parametrize("runtime_type_checker", ["beartype"])
def test_args_with_unpack(runtime_type_checker: AVAILABLE_TYPE_CHECKERS):
    @typing_extensions.overload
    def my_function(*args: Unpack[tuple[int, int, int]]) -> str:
        red, green, blue = args
        return f"#{red:02x}{green:02x}{blue:02x}"

    @typing_extensions.overload
    def my_function(*args: Unpack[tuple[str, float, int]]) -> str:
        return f"{args[0]}{args[1] * args[2]}"

    @overtake(runtime_type_checker=runtime_type_checker)
    def my_function(*args) -> str:
        ...

    assert my_function(0, 255, 128) == "#00ff80"
    assert my_function("Hello", 1.23, 2) == "Hello2.46"


@pytest.mark.parametrize("runtime_type_checker", ["pydantic"])
def test_kwargs(runtime_type_checker: AVAILABLE_TYPE_CHECKERS):
    @typing_extensions.overload
    def my_function(**kwargs: int) -> int:
        return sum(kwargs.values())

    @typing_extensions.overload
    def my_function(**kwargs: str) -> str:
        return "".join(kwargs.values())

    @overtake(runtime_type_checker=runtime_type_checker)
    def my_function(**kwargs) -> str | int:
        ...

    assert my_function(a="5153", b="dododo") == "5153dododo"
    assert my_function(a=3, b=3) == 6


@pytest.mark.parametrize("runtime_type_checker", ["pydantic"])
def test_kwargs_with_typeddict(runtime_type_checker: AVAILABLE_TYPE_CHECKERS):
    class MyDict1(TypedDict):
        a: int
        b: int

    class MyDict2(TypedDict):
        c: int
        d: int

    @typing_extensions.overload
    def my_function(**kwargs: Unpack[MyDict1]) -> int:
        return kwargs["a"]

    @typing_extensions.overload
    def my_function(**kwargs: Unpack[MyDict2]) -> int:
        return kwargs["c"]

    @overtake(runtime_type_checker=runtime_type_checker)
    def my_function(**kwargs) -> int:
        ...

    assert my_function(a=1, b=2) == 1
    assert my_function(c=3, d=4) == 3


@pytest.mark.parametrize("runtime_type_checker", ["pydantic"])
def test_kwargs_with_one_typeddict(runtime_type_checker: AVAILABLE_TYPE_CHECKERS):
    class MyDict1(TypedDict):
        a: int
        b: str

    @typing_extensions.overload
    def my_function(a: int, b: int) -> int:
        return a

    @typing_extensions.overload
    def my_function(**kwargs: Unpack[MyDict1]) -> str:
        return kwargs["b"]

    @overtake(runtime_type_checker="pydantic")
    def my_function(a: int, b: int | str) -> int | str:
        ...

    assert my_function(a=1, b=2) == 1
    assert my_function(a=3, b="Hello") == "Hello"
