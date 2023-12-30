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


class DataFilesAttributesPuzzle:
    puzzle_id_col_name: str
    puzzle_puzzle_type_col_name: str
    puzzle_solution_state_col_name: str
    puzzle_initial_state_col_name: str
    puzzle_num_wildcards_col_name: str


class DataFilesAttributesPuzzleInfo:
    puzzle_info_puzzle_type_col_name: str
    puzzle_info_allowed_moves_col_name: str


class DataFilesAttributesSubmission:
    submission_id_col_name: str
    submission_moves_col_name: str


class DataFiles:
    puzzles_file: str
    puzzles_info_file: str
    submission_file: str
    puzzle_attributes: DataFilesAttributesPuzzle
    puzzle_info_attributes: DataFilesAttributesPuzzleInfo
    submission_attributes: DataFilesAttributesSubmission


@dataclass
class TrainConfig:
    dir: DirConfig
    config: RunConfig
    data: DataFiles
