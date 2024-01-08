from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import numpy.typing as npt

from src.puzzles.PuzzleTools import PuzzleTools


@dataclass
class PuzzleDTO(PuzzleTools):
    """
    contains the necessary attributes about a given puzzle
    """

    pid: int
    state: str
    allowed_moves: Dict[str, npt.NDArray[np.int32]]
    solution_state: str
    initial_state: str
    num_wildcards: int
    submission_solution: str
    max_moves: int
    previous_states: List[str]
    previous_moves: List[str]

    def __init__(
        self,
        pid,
        allowed_moves,
        solution_state,
        initial_state,
        num_wildcards,
        submission_solution,
        max_moves,
    ):
        super().__init__()
        self.pid = pid
        self.allowed_moves = allowed_moves
        self.solution_state = solution_state
        self.initial_state = initial_state
        self.num_wildcards = num_wildcards
        self.submission_solution = submission_solution
        self.max_moves = max_moves
        self.previous_states = []
        self.previous_moves = []

        self.state = self.initial_state
    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return f"PuzzleDTO(pid={self.pid}, state={self.state})"
