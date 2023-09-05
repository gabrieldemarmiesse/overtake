from typing import Callable


def get_fully_qualified_name(obj: Callable) -> str:
    return f"{obj.__module__}.{obj.__qualname__}"
