import datetime
from dataclasses import dataclass
from typing import List

from src.dtos.PuzzleDTO import PuzzleDTO


@dataclass
class ResultDTO:
    """
    result of running a puzzle
    """
    puzzle_id: int
    puzzle: PuzzleDTO
    score: float
    solved: bool
    time_taken: datetime.timedelta
    end_state: List[str]
    error_count: int
    move_to_error_mapping: list
