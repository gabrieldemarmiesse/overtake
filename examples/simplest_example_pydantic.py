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
def connect(arg):
    ...


print(connect("rediss://:pass@localhost"))
# Connected to redis!
print(connect("mongodb://mongodb0.example.com:27017"))
# Connected to MongoDB!
