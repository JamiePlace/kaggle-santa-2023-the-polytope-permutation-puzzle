# TODO update to use pydantic
from dataclasses import dataclass


@dataclass
class DataClass1:
    key1: int
    key2: float
    key3: bool


@dataclass
class DataClass2:
    key4: list[int]
    dc: DataClass1


@dataclass
class DataConfig:
    batch_size: int
    window_size: int


@dataclass
class TrainConfig:
    learning_rate: float
    dataconf: DataConfig


@dataclass
class InferenceConfig:
    learning_rate: float
    dataconf: DataConfig
