import logging
from abc import abstractmethod
from typing import List

import pandas as pd

from src.conf import TrainConfig
from src.dtos.PuzzleDTO import PuzzleDTO

LOGGER = logging.getLogger()


class MoveSetGeneratorBase:
    cfg: TrainConfig
    puzzles: List[PuzzleDTO]

    def __init__(self, training_config: TrainConfig):
        self.cfg = training_config

    @abstractmethod
    def generate_moveset(self):
        pass

    def to_csv(self, fname: str = "submission.csv"):
        puzzle_id = []
        puzzle_solution = []
        for puzzle in self.puzzles:
            puzzle_id.append(puzzle.pid)
            puzzle_solution.append(".".join(puzzle.moves))
        df = pd.DataFrame({"id": puzzle_id, "moves": puzzle_solution})
        df.to_csv(fname, index=False)
