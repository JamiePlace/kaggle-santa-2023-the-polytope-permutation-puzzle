# TODO update to use pydantic
from dataclasses import dataclass


@dataclass
class DataClass1:
    key1: int
    key2: float
    key3: bool


class DataClass2:
    key4: list[int]
    dc: DataClass1
