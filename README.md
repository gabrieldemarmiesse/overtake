# Overtake

## How to install?
```bash
pip install overtake
```

Overtake is quite self-contained. The only dependency, by default, is `typing-extensions`.

## What is Overtake?

Have you ever dreamed of declaring the same function multiple times?
```python
def count_words(arg: str) -> int:
    return len(arg.split())


def count_words(arg: list[str]) -> int:
    return sum(len(text.split()) for text in arg)


print(count_words("one two three!"))
# 3
print(count_words(["one two", "three four five six"]))
# 6
```

Well you are at the right place!

Overtake is a small library made to push `@typing.overload` even further.
`@typing.overload` just defines signatures, so that type checkers know what type hints
are available when calling a function.
With Overtake, you can also call those functions at runtime, similar to languages like
C++ or Julia.

An example is worth a thousand words:

```python
from typing import overload

# if you are using Python <3.11, you'll need instead
# from typing_extensions import overload

from overtake import overtake


@overload
def count_words(arg: str) -> int:
    return len(arg.split())


@overload
def count_words(arg: list[str]) -> int:
    return sum(len(text.split()) for text in arg)


@overtake(runtime_type_checker="beartype")
def count_words(arg):
    ...


print(count_words("one two three!"))
# 3
print(count_words(["one two", "three four five six"]))
# 6
```

Overtake will analyse the types and provided arguments to call the right implementation.

It works for every signature supported by [`@typing.overload`](https://docs.python.org/3/library/typing.html#typing.overload)

This pattern is supported by IDEs (Pycharm, VSCode, etc...) so autocompletion will work well.
It's also supported as well by type checkers (Mypy, Pyright, etc...) so you don't need to compromise on type safety 😁

Overtake follow closely the Mypy guide on `@typing.overload`: https://mypy.readthedocs.io/en/stable/more_types.html#function-overloading

## More advanced examples.

We can show you here more pattern that are possible. Basically `if isinstance(..., ...)` might be your cue that
`overtake` might help you write clearer code.

### Recursivity

Let's write a function that returns the number of days since January 1st:

```python
from typing import overload
from datetime import date

from overtake import overtake


@overload
def days_this_year(current_date: date) -> int:
    delta = current_date - date(2023, 1, 1)
    return delta.days


@overload
def days_this_year(current_date: str) -> int:
    return days_this_year(date.fromisoformat(current_date))


@overtake
def days_this_year(current_date):
    ...


print(days_this_year(date(2023, 8, 15)))
# 226
print(days_this_year("2023-08-15"))
# 226
```

You can call your function in a recursive manner, to deduplicate code. We could actually rewrite our first example like this:

```python
from typing import overload

from overtake import overtake


@overload
def count_words(input_value: str) -> int:
    return len(input_value.split())


@overload
def count_words(input_value: list[str]) -> int:
    return sum(count_words(text) for text in input_value)


@overtake(runtime_type_checker="beartype")
def count_words(input_value):
    ...


print(count_words("one two three!"))
# 3
print(count_words(["one two", "three four five six"]))
# 6
```

### Different output types

It's also possible to have different output types, like with `@overload`


```python
from typing import overload

from overtake import overtake


@overload
def convert_to_int(input_value: str) -> int:
    return int(input_value)


@overload
def convert_to_int(input_value: list[str]) -> list[int]:
    return [int(x) for x in input_value]


@overtake(runtime_type_checker="beartype")
def convert_to_int(input_value):
    ...


print(convert_to_int("88"))
# 88 (an integer)
print(convert_to_int(["88", "42", "84"]))
# [88, 42, 84] (a list of integers)
```


### Leveraging optional arguments

It can avoid some annoying uses of `if ... is None:`, you can specify different number of arguments (but the order must match!).

For this example, let's say that you want the user to be able to write some text in any kind of file.
If the file is not provided, we create a temporary file.
We must accept any input for the file. A `str`, a `pathlib.Path`, a file-like object too. Or nothing (random file).

```python
from typing import overload
from pathlib import Path
import io
import random

from overtake import overtake


@overload
def write_text_to_file(text: str, file: io.TextIOBase) -> None:
    file.write(text)


@overload
def write_text_to_file(text: str, file: Path) -> Path:
    file.write_text(text)
    return file


@overload
def write_text_to_file(text: str, file: str) -> Path:
    return write_text_to_file(text, Path(file))


@overload
def write_text_to_file(text: str) -> Path:
    random_file_name = f"/tmp/{random.randint(0, 10)}.txt"
    return write_text_to_file(text, random_file_name)


@overtake(runtime_type_checker="beartype")
def write_text_to_file(text, file=None):
    ...


print(write_text_to_file("hello world"))
# /tmp/4.txt
print(write_text_to_file("hello world", "/tmp/some-file.txt"))
# /tmp/some-file.txt
print(write_text_to_file("hello world", Path("/tmp/some-file.txt")))
# /tmp/some-file.txt
print(write_text_to_file("hello world", io.StringIO()))
# None (we didn't write in a file on disk)
```

### Leveraging keyword arguments

You can use this paradigm to force the user to use less arguments than the number defined in the function.
Here is an example where you're looking for the balance of a user. You can provide the user id, or the user's name,
but not both.

```python
from overtake import overtake
from typing import overload


@overload
def find_user_balance(name: str) -> int:
    return 40


@overload
def find_user_balance(user_id: int) -> int:
    return 50


@overtake
def find_user_balance(*, user_id=None, name=None):
    ...


print(find_user_balance(name="Julie"))
# 40
print(find_user_balance(user_id=14))
# 50
```

In this situation, Overtake saves you quite some time. You don't have to check that
`user_id` and `name`are both provided, and don't have to check that none of them has been provided.
Overtake does this for you!

## Recommendations

We recommend using a type checker of your choice (Mypy, Pyright, etc...) so that the type checker catches
invalid usages of `@overload`. Even though it's not mandatory, it's helpful to catch mistakes with `@overload` early.


## The argument `runtime_type_checker`

Runtime type checking in Python is difficult. Actually, very difficult. A few libraries provide this functionality, like
[beartype](https://beartype.readthedocs.io/en/latest/) or [pydantic](https://docs.pydantic.dev/latest/).

To avoid having to install any dependency, `overtake` can use `isinstance` as the default `"basic"` type checker.
Note that this will only work with types that are classes. For example, it won't work with `list[str]` but it will work with `list` or
`datetime`.

To handle more complicated types, you should use

```python
@overtake(runtime_type_checker="beartype")
def find_user_balance(*, user_id=None, name=None):
    ...
```
or
```python
@overtake(runtime_type_checker="pydantic")
def find_user_balance(*, user_id=None, name=None):
    ...
```

####  What `runtime_type_checker` do I need? There are so many choices!!!

First of all, don't pick any (`"basic"` will be used by default) and see if it works.
If the types you are using are too complicated (if you are using generics or protocols),
overtake will raise an error and tell you to use another `runtime_type_checker`.

Then you have the choice between `"beartype"` and `"pydantic"`. Ask yourself the question,
"Do I need beartype-specific types? Like [beartype's validators](https://beartype.readthedocs.io/en/latest/api_vale/)?"
If yes, use beartype.

If not, ask yourself the question
"Do I need Pydantic's specific types? Like [Pydantic's urls or custom types](https://docs.pydantic.dev/latest/usage/types/custom/#custom-data-types)?"
If yes, use pydantic.

If you are still undecided after this, you should use beartype as it's faster (validate in O(1)), but beware,
you might get silent errors for unsupported types, and it might be really unpleasant.
See [this issue](https://github.com/beartype/beartype/issues/279).
Pydantic might be slower, but you'll get errors when using an unsupported type. So it's safer.

Both are really cool libraries, I encourage any curious mind to go read those docs!
We recommend you install those libs with `pip install overtake[beartype]` or `pip install overtake[pydantic]`.

#### What cool stuff can I do with the Beartype type checker?

I was waiting for you to ask. Lo and behold!

```python
from overtake import overtake
from typing import overload, Annotated
from beartype.vale import Is

# Type hint matching only strings with lengths ranging [4, 40].
LengthyString = Annotated[str, Is[lambda text: 4 <= len(text) < 40]]

# Type hint matching only strings with lengths ranging [0, 4].
ShortString = Annotated[str, Is[lambda text: 0 <= len(text) < 4]]


@overload
def is_this_string_big(arg: ShortString) -> str:
    return "This is a short string!"


@overload
def is_this_string_big(arg: LengthyString) -> str:
    return "This is a very long string"


@overtake(runtime_type_checker="beartype")
def is_this_string_big(arg):
    ...


print(is_this_string_big("Hi!"))
# This is a short string!
print(is_this_string_big("No one expects the spanish inquisition!"))
# This is a very long string
```

Do you even need `if` statements anymore? One can wonder.

#### What cool stuff can I do with the Pydantic type checker?

You can have fun with their custom types!

```python
from typing import overload

from overtake import overtake
from pydantic import MongoDsn, RedisDsn


@overload
def connect(arg: RedisDsn) -> str:
    return "Connected to redis!"


@overload
def connect(arg: MongoDsn) -> str:
    return "Connected to MongoDB!"


@overtake(runtime_type_checker="pydantic")
def connect(arg):
    ...


print(connect("rediss://:pass@localhost"))
# Connected to redis!
print(connect("mongodb://mongodb0.example.com:27017"))
# Connected to MongoDB!
```

## Compatibility with Pyright

Pyright has a small compatibility issue, you might get the following error:
```
error: "my_function" is marked as overload, but it includes an implementation
The body of a function overload should be "..."
```
This can be fixed without disabling type checking on calls and function bodies by adding `# type: ignore`
next to the overloaded function signatures. Here is a small example:

```python
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
```

To solve this limitation in the long run (Mypy might one day raise the same type of errors),
a draft PEP has been made. Don't hesitate to give feedback in the discussion!
* [The PEP to offically support multiple dispatch](https://github.com/gabrieldemarmiesse/PEP-draft-multiple-dispatcher)
* [Discourse discussion](https://discuss.python.org/t/multiple-dispatch-based-on-typing-overload/26197)

