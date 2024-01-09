import logging
from abc import abstractmethod
from typing import List

import pandas as pd

from src.conf import TrainConfig
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO

LOGGER = logging.getLogger()


class MoveSetGeneratorBase:
    cfg: TrainConfig
    movesetDTO: MovesetDTO
    solutions: dict
    puzzles: List[PuzzleDTO]

    def __init__(self, training_config: TrainConfig):
        self.cfg = training_config
        solutions = pd.read_csv(self.cfg.data.submission_file)
        self.solutions = self.__convert_to_dict(solutions)

    @abstractmethod
    def generate_moveset(self) -> MovesetDTO:
        pass

    def to_csv(self, fname: str = "submission.csv"):
        puzzle_id = []
        puzzle_solution = []
        for puzzle in self.puzzles:
            puzzle_id.append(puzzle.pid)
            puzzle_solution.append(puzzle.submission_solution)
        df = pd.DataFrame({"id": puzzle_id, "moves": puzzle_solution})
        df.to_csv(fname, index=False)

    def __convert_to_dict(self, df: pd.DataFrame) -> dict:
        output = {}
        ids = df.id.values
        moves = df.moves.values
        for id, move in zip(ids, moves):
            output[id] = move
        return output
