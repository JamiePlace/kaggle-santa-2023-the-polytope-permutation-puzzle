from ast import mod
import logging
from abc import abstractmethod
from pathlib import Path

import pandas as pd

from src.conf import TrainConfig
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.ResultDTO import ResultDTO
from src.dtos.ResultsDTO import ResultsDTO

LOGGER = logging.getLogger()


class MoveSetGeneratorBase:
    cfg: TrainConfig
    previous_results: ResultsDTO
    specific_puzzle: int
    puzzle_type: str
    movesetDTO: MovesetDTO

    def __init__(self, training_config: TrainConfig, resultsDTO: ResultsDTO | None):
        self.cfg = training_config
        self.previous_results = resultsDTO

        self.solution = pd.read_csv(Path(self.cfg.data.puzzles_file))
        self.submission = pd.read_csv(Path(self.cfg.data.submission_file))
        self.puzzle_info = pd.read_csv(
            Path(self.cfg.data.puzzles_info_file),
            index_col=self.cfg.data.puzzle_info_attributes.puzzle_info_puzzle_type_col_name,
        )
        self.puzzle_type = self.cfg.config.puzzle_type

    @abstractmethod
    def generate_moveset(self) -> MovesetDTO:
        pass

    def with_specific_puzzle(self, specific_puzzle):
        self.specific_puzzle = specific_puzzle

    def find_previous_specific_puzzle(self) -> ResultDTO:
        previous_result = None

        for result in self.previous_results.results:
            if result.puzzle_id == self.specific_puzzle:
                previous_result = result

        return previous_result
    def to_csv(self, fname: str = "submission.csv"):
        puzzle_id = []
        puzzle_solution = []
        for puzzle in self.movesetDTO.puzzles:
            puzzle_id.append(puzzle.puzzle_id)
            puzzle_solution.append(puzzle.submission_solution)
        df = pd.DataFrame({'id': puzzle_id, 'moves': puzzle_solution})
        df.to_csv(fname, index=False)
