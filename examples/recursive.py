from datetime import date

from overtake import overtake
from typing_extensions import overload


@overload
def days_this_year(current_date: date) -> int:  # type: ignore
    delta = current_date - date(2023, 1, 1)
    return delta.days


@overload
def days_this_year(current_date: str) -> int:  # type: ignore
    return days_this_year(date.fromisoformat(current_date))


@overtake
def days_this_year(current_date):
    ...


print(days_this_year(date(2023, 8, 15)))
# 226
print(days_this_year("2023-08-15"))
# 226
