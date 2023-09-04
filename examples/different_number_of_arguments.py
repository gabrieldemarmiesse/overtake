import io
from pathlib import Path
import random

from overtake import overtake
from typing_extensions import overload


class Something(str):
    pass


@overload
def write_text_to_file(text: str) -> Path:  # type: ignore
    random_file_name = f"/tmp/{random.randint(0, 10)}.txt"
    return write_text_to_file(text, random_file_name)


@overload
def write_text_to_file(text: str, file: str) -> Path:  # type: ignore
    return write_text_to_file(text, Path(file))


@overload
def write_text_to_file(text: str, file: Path) -> Path:  # type: ignore
    file.write_text(text)
    return file


@overload
def write_text_to_file(text: str, file: io.TextIOBase) -> None:  # type: ignore
    file.write(text)


@overtake
def write_text_to_file(text, file=None):
    ...


print(write_text_to_file(Something("hello world"), Something("dodo")))
# /tmp/4.txt
print(write_text_to_file("hello world", "/tmp/some-file.txt"))
print(write_text_to_file("hello world", "dodo"))
# /tmp/some-file.txt
print(write_text_to_file("hello world", Path("/tmp/some-file.txt")))
# /tmp/some-file.txt
print(write_text_to_file("hello world", io.StringIO()))
# None (we didn't write in a file on disk)
