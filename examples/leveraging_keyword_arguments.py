from overtake import overtake
from typing_extensions import overload


@overload
def find_user_balance(name: str) -> int:  # type: ignore
    return 40


@overload
def find_user_balance(user_id: int) -> int:  # type: ignore
    return 50


@overtake
def find_user_balance(*, user_id=None, name=None):
    ...


print(find_user_balance(user_id=14))
# 40
print(find_user_balance(name="Julie"))
# 50
