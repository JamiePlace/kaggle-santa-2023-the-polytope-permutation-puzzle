from dataclasses import dataclass
import logging
import pandas as pd

LOGGER = logging.getLogger()


@dataclass
class MovesetDTO:
    """
    defines the data required to score a puzzle
    """
    solution: pd.DataFrame
    submission: pd.DataFrame
    puzzle_info: pd.DataFrame

    series_id_column_name: str
    moves_column_name: str

    def __init__(self, solution, submission, puzzle_info):
        self.solution = solution
        self.submission = submission
        self.puzzle_info = puzzle_info

        self.series_id_column_name = "id"
        self.moves_column_name = "moves"
