# TODO update to use pydantic
from dataclasses import dataclass


@dataclass
class DirConfig:
    data_dir: str
    processed_dir: str
    output_dir: str
    model_dir: str
    sub_dir: str


@dataclass
class RunConfig:
    specific_puzzle: int
    generations: int


class DataFiles:
    puzzle_info: str
    solution: str
    submission: str


@dataclass
class TrainConfig:
    dir: DirConfig
    config: RunConfig
    data: DataFiles
