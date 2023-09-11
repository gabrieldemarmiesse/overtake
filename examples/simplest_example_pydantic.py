from overtake import overtake
from pydantic import MongoDsn, RedisDsn
from typing_extensions import overload


@overload
def connect(arg: RedisDsn) -> str:  # type: ignore
    return "Connected to redis!"


@overload
def connect(arg: MongoDsn) -> str:  # type: ignore
    return "Connected to MongoDB!"


@overtake(runtime_type_checker="pydantic")
def connect(arg):  # type: ignore
    ...


print(connect("rediss://:pass@localhost"))  # type: ignore
# Connected to redis!
print(connect("mongodb://mongodb0.example.com:27017"))  # type: ignore
# Connected to MongoDB!
