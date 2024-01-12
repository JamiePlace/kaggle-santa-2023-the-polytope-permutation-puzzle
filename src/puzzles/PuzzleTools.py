from typing import Dict, List

import numpy as np
import numpy.typing as npt
from tqdm import tqdm


class PuzzleTools:
    allowed_moves: Dict[str, npt.NDArray[np.int32]]
    previous_states: List[str]
    moves: List[str]
    solution_state: str
    num_wildcards: int
    state: str

    def __init__(self):
        pass

    def apply_moves(self, moves: str):
        moves = moves.split(".")  # type: ignore
        start_state = self.state
        self.moves.extend(moves)

        states = np.empty((len(moves)), dtype=list)
        states[0] = start_state
        state = np.array(start_state.split(";"))
        for i, move in tqdm(
            enumerate(moves), desc="Applying moves", total=len(moves), leave=False
        ):
            move_list = self.allowed_moves[move]
            state = state[move_list]
            states[i] = ";".join(state)

        self.previous_states.extend(states[:-1])
        self.state = states[-1]
        
    def validate(self):
        solved = self.state == self.solution_state
        state_list = np.array(self.state.split(";"))
        solution_state_list = np.array(self.solution_state.split(";"))
        wildcard_count = np.sum(state_list != solution_state_list)

        if solved and wildcard_count <= self.num_wildcards:
            return True
        return False
