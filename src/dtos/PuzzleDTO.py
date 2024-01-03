from dataclasses import dataclass
from typing import Dict, List

from src.dtos.PuzzleStateChangeDTO import PuzzleStateChangeDTO


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
    previous_state: PuzzleStateChangeDTO | None

    def __init__(self, puzzle_id, allowed_moves, solution_state, initial_state, num_wildcards, submission_solution,
                 max_moves):
        self.puzzle_id = puzzle_id
        self.allowed_moves = allowed_moves
        self.solution_state = solution_state
        self.initial_state = initial_state
        self.num_wildcards = num_wildcards
        self.submission_solution = submission_solution
        self.max_moves = max_moves
        self.previous_state = None
