import numpy as np
import numpy.typing as npt
from typing import Dict, List
class PuzzleTools:
    allowed_moves: Dict[str, npt.NDArray[np.int32]]
    previous_states: List[str]
    previous_moves: List[str]
    def __init__(self):
        pass
    def apply_move(self, move:str):
        self.previous_states.append(self.state)
        self.previous_moves.append(move)
        move_list = self.allowed_moves[move]
        self.state = ";".join(np.array(self.state.split(";"))[move_list])

