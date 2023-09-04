import timeit

from overtake import overtake
from typing_extensions import overload


def baseline_function(
    arg1: list[str] | list[int],
    arg2: str,
    arg3: str,
    arg4: tuple,
    arg5: int,
    arg6: list[int],
):
    if isinstance(arg1[0], str):
        pass
    elif isinstance(arg1[0], int):
        pass
    else:
        pass


@overload
def overtake_function(
    arg1: list[str], arg2: str, arg3: str, arg4: tuple, arg5: int, arg6: list[int]
):
    pass


@overload
def overtake_function(
    arg1: list[int], arg2: str, arg3: str, arg4: tuple, arg5: int, arg6: list[int]
):
    pass


@overtake
def overtake_function(arg1, arg2, arg3, arg4, arg5, arg6):
    ...


big_list_int = [4] * 10_000


baseline_time = timeit.timeit(
    "baseline_function(big_list_int, '', '', (1,), 2, big_list_int)",
    number=1000,
    globals=globals(),
)

print("Baseline:", baseline_time)

# trigger first time computation
overtake_function(big_list_int, "", "", (1,), 2, big_list_int)

overtake_time = timeit.timeit(
    "overtake_function(big_list_int, '', '', (1,), 2, big_list_int)",
    number=1000,
    globals=globals(),
)
print("Overtake:", overtake_time)

print(f"Overtake is {overtake_time / baseline_time} times slower than 'isisntance'.")
