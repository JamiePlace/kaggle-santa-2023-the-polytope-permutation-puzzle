import numpy as np
import numpy.typing as npt
from typing import Dict, List
class PuzzleTools:
    allowed_moves: Dict[str, npt.NDArray[np.int32]]
    previous_states: List[str]
    moves: List[str]
    solution_state: str
    num_wildcards: int
    def __init__(self):
        pass

    def apply_moves(self, moves: str):
        if len(moves.split(".")) == 1:
            self.__apply_move(moves)
            return 

        for move in moves.split("."):
            self.__apply_move(move)

    def __apply_move(self, move:str):
        self.previous_states.append(self.state)
        self.moves.append(move)
        move_list = self.allowed_moves[move]
        self.state = ";".join(np.array(self.state.split(";"))[move_list])
    
    def validate(self):
        solved = self.state == self.solution_state
        state_list = np.array(self.state.split(";"))
        solution_state_list = np.array(self.solution_state.split(";"))
        wildcard_count = np.sum(state_list != solution_state_list)

        if solved and wildcard_count <= self.num_wildcards:
            return True
        return False


