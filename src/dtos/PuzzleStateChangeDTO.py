from dataclasses import dataclass
from typing import List


@dataclass
class PuzzleStateChangeDTO:
    """
    contains the necessary attributes about a given puzzle
    """
    puzzle_id: int
    initial_state: List[str]
    after_state: List[str]
    solution_used: str
    error_count: int
    move_to_error_mapping: list
    attempt: int
