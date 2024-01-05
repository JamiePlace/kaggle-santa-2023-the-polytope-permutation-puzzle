from src.puzzles.puzzle_solver_base import PuzzleSolverBase
from src.utilities.puzzle_utils import calculate_cube_face_error


class FacePuzzleSolver(PuzzleSolverBase):
    """
    all logic is in the base for now,
    we can look at ways to make this faster and build on new classes if needed...
    """
    face_to_score: str
    use_wildcards: bool

    def __init__(self, face_to_score: str):
        self.face_to_score = face_to_score
        self.use_wildcards = False

    def get_scoring_method(self, solution, end_state):
        return calculate_cube_face_error(solution, end_state, self.face_to_score)

    def is_puzzle_solved(self, num_wrong_facelets, num_wildcards):
        """
        for now do not use the num wildcards, as this is a part solve

        maybe later we can say for this parital solution either allow all wildcards to be used or some of it
        """
        if self.use_wildcards:
            solved: bool
            if num_wrong_facelets > num_wildcards:
                solved = False
            else:
                solved = True
            return solved
        else:
            return num_wrong_facelets == 0
