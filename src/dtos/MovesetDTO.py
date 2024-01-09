import logging
from dataclasses import dataclass

import pandas as pd

from src.conf import TrainConfig

LOGGER = logging.getLogger()


@dataclass
class MovesetDTO:
    """
    defines the data required to score a puzzle
    """
    moves: list

    def __init__(self, cfg: TrainConfig, pid: int, empty: bool = False):
        self.cfg = cfg
        if empty:
            self.moves = []
        else:
            solution = pd.read_csv(self.cfg.data.submission_file)
            solution = solution.loc[solution["id"] == pid]
            self.moves = solution["moves"].values[0].split(".")

    def __iter__(self):
        return iter(self.moves)


