import logging
from typing import Optional
from src.utils import cancel_pairs
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.puzzles.sample_puzzle_solver import SamplePuzzleSolver

LOGGER = logging.getLogger()


class LoopRemovalMovesetGenerator(MoveSetGeneratorBase):
    """
    Building on SimpleMoveSetGenerator, this class will remove loops from the submission
    """

    movesetDTO: MovesetDTO
    puzzle_type: str
    specific_puzzle: int

    def __init__(self, cfg, resultsDTO: Optional[ResultsDTO] = None):
        super().__init__(cfg, resultsDTO)
        self.movesetDTO = MovesetDTO(self.solution, self.submission, self.puzzle_info)
        self.remove_loops()

    def remove_loops(self):
        LOGGER.info(f"--- Generating moveset using LoopRemovalMovesetGenerator ---")

        puzzles = []
        for sol, sub in zip(self.solution.itertuples(), self.submission.itertuples()):
            puzzle = self.__convert_dict_to_puzzle(self.puzzle_info, sol, sub)
            if puzzle is not None:
                puzzles.append(puzzle)


        self.movesetDTO.set_puzzles(puzzles)

        LOGGER.info(f"--- Generating moveset complete---\n")

    def __convert_dict_to_puzzle(self, puzzle_info, sol, sub):
        solver = SamplePuzzleSolver()
        puzzle_id = int(getattr(sol, self.cfg.data.puzzle_attributes.puzzle_id_col_name))
        puzzle_type = str(
            getattr(sol, self.cfg.data.puzzle_attributes.puzzle_puzzle_type_col_name)
        )
        puzzle_type = puzzle_type.split("_")[0]
        assert puzzle_id == int(
            getattr(sub, self.cfg.data.submission_attributes.submission_id_col_name)
        )

        # break out early if you dont want to wait for ages
        if self.cfg.config.specific_puzzle is not None:
            if puzzle_id != self.cfg.config.specific_puzzle:
                return None
        if self.cfg.config.puzzle_type is not None:
            if puzzle_type != self.cfg.config.puzzle_type:
                return None

        sub_solution = getattr(sub, self.cfg.data.submission_attributes.submission_moves_col_name)
        puzzle = self.generate_puzzle(puzzle_id, puzzle_info, sol, sub_solution)
        if puzzle_type == "cube":
            try:
                new_solution = cancel_pairs(sub_solution)
                
                puzzle = self.generate_puzzle(puzzle_id, puzzle_info, sol, new_solution)
                # this will raise an error if the solution is invalid
                _ = solver.score_puzzle(puzzle, validate=True)
                sub_solution = new_solution

            except:
                puzzle = self.generate_puzzle(puzzle_id, puzzle_info, sol, sub_solution)
        if puzzle_type == "wreath":
            puzzle = self.generate_puzzle(puzzle_id, puzzle_info, sol, sub_solution)
        if puzzle_type == "globe":
            puzzle = self.generate_puzzle(puzzle_id, puzzle_info, sol, sub_solution)

        return puzzle

