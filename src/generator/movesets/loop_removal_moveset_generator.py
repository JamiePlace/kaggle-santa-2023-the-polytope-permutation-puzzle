import logging
from typing import List
from src.utils import cancel_pairs
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase

LOGGER = logging.getLogger()


class LoopRemovalMovesetGenerator(MoveSetGeneratorBase):
    """
    Building on SimpleMoveSetGenerator, this class will remove loops from the submission
    """

    movesetDTO: MovesetDTO
    puzzle_type: str
    specific_puzzle: int
    puzzles: List[PuzzleDTO]

    def __init__(self, cfg, puzzles: List[PuzzleDTO]):
        super().__init__(cfg)
        self.puzzles = puzzles
        self.remove_loops()

    def remove_loops(self):
        LOGGER.info(f"--- Generating moveset using LoopRemovalMovesetGenerator ---")

        new_puzzle_states = []
        for puzzle in self.puzzles:
            current_solution = puzzle.moves
            current_state = puzzle.initial_state
            if puzzle.ptype == "cube":
                new_solution = cancel_pairs(puzzle.moves)
                puzzle.moves = []
                puzzle.state = puzzle.initial_state
                puzzle.apply_moves(new_solution)
                if not puzzle.validate():
                    puzzle.moves = current_solution
                    puzzle.state = current_state
            new_puzzle_states.append(puzzle)
        self.puzzles = new_puzzle_states

        LOGGER.info(f"--- Generating moveset complete---\n")
