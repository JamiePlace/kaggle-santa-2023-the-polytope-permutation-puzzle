import logging
from dataclasses import dataclass
from typing import Dict, List

LOGGER = logging.getLogger()


@dataclass
class PuzzleDTO:
    """
    contains the necessary attributes about a given puzzle
    """
    puzzle_id: int
    allowed_moves: Dict[str, List[int]]
    solution_state: List[str]
    initial_state: List[str]
    num_wildcards: int
    submission_solution: str
    max_moves: int
