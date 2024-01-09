from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import numpy.typing as npt

from src.puzzles.PuzzleTools import PuzzleTools
from src.dtos.MovesetDTO import MovesetDTO


@dataclass
class PuzzleDTO(PuzzleTools):
    """
    contains the necessary attributes about a given puzzle

    Atrtributes:
    ------------
        pid: int
            the puzzle id
        ptype: str
            the puzzle type
        state: str
            the current state of the puzzle
        allowed_moves: Dict[str, npt.NDArray[np.int32]]
            the allowed moves for the puzzle
        solution_state: str
            the solution state of the puzzle
        initial_state: str
            the initial state of the puzzle
        num_wildcards: int
            the number of wildcards in the puzzle
        moves: MovesetDTO
            the moves made to achieve the current state

    """

    pid: int
    ptype: str
    state: str
    allowed_moves: Dict[str, npt.NDArray[np.int32]]
    solution_state: str
    initial_state: str
    num_wildcards: int
    previous_states: List[str]
    moves: List[str]


    def __init__(
        self,
        pid,
        ptype,
        allowed_moves,
        solution_state,
        initial_state,
        num_wildcards,
    ):
        """
        Initialises the PuzzleDTO class

        Parameters:
            pid: int
                the puzzle id
            allowed_moves: Dict[str, npt.NDArray[np.int32]]
                the allowed moves for the puzzle
            solution_state: str
                the solution state of the puzzle
            initial_state: str
                the initial state of the puzzle
            num_wildcards: int
                the number of wildcards in the puzzle
            moves: MovesetDTO
                the moves made to achieve the current state
        """
        super().__init__()
        self.pid = pid
        self.ptype = ptype
        self.allowed_moves = allowed_moves
        self.solution_state = solution_state
        self.initial_state = initial_state
        self.num_wildcards = num_wildcards
        self.state = self.initial_state
        self.previous_states = []
        self.moves = []
    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        return f"PuzzleDTO(pid={self.pid}, state={self.state})"
