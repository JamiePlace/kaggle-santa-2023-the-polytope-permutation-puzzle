import logging
from dataclasses import dataclass
from typing import List

import pandas as pd

from src.dtos.PuzzleDTO import PuzzleDTO

LOGGER = logging.getLogger()


@dataclass
class MovesetDTO:
    """
    defines the data required to score a puzzle
    """
    solution: pd.DataFrame
    submission: pd.DataFrame
    puzzle_info: pd.DataFrame
    puzzles: List[PuzzleDTO]

    series_id_column_name: str
    moves_column_name: str
    allowed_moves_column_name: str

    def __init__(self, solution, submission, puzzle_info):
        self.solution = solution
        self.submission = submission
        self.puzzle_info = puzzle_info
        self.puzzles = []

        self.series_id_column_name = "id"
        self.moves_column_name = "moves"
        self.allowed_moves_column_name = "allowed_moves"

    def set_puzzles(self, puzzles):
        self.puzzles = puzzles
