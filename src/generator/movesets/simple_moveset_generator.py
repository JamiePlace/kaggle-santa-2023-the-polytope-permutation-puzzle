import logging
from ast import literal_eval
from typing import Optional

from sympy.combinatorics import Permutation

from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase

LOGGER = logging.getLogger()


class SimpleMoveSetGenerator(MoveSetGeneratorBase):
    """
    OOTB moveset generator taking moveset from file.
    """

    movesetDTO: MovesetDTO
    puzzle_type: str
    specific_puzzle: int

    def __init__(self, cfg, resultsDTO: Optional[ResultsDTO] = None):
        super().__init__(cfg, resultsDTO)

        LOGGER.info(f"--- Generating moveset using SimpleMoveSetGenerator ---")

        self.movesetDTO = MovesetDTO(self.solution, self.submission, self.puzzle_info)
        puzzles = []
        for sol, sub in zip(self.solution.itertuples(), self.submission.itertuples()):
            puzzle = self.__convert_dict_to_puzzle(self.puzzle_info, sol, sub)
            if puzzle is not None:
                puzzles.append(puzzle)

        self.movesetDTO.set_puzzles(puzzles)

        LOGGER.info(f"--- Generating moveset complete---\n")

    def generate_moveset(self):
        LOGGER.info(f"--- Generating moveset using SimpleMoveSetGenerator ---")

        move_set = MovesetDTO(self.solution, self.submission, self.puzzle_info)

        puzzles = []
        for sol, sub in zip(self.solution.itertuples(), self.submission.itertuples()):
            puzzle = self.__convert_dict_to_puzzle(self.puzzle_info, sol, sub)
            if puzzle is not None:
                puzzles.append(puzzle)

        move_set.set_puzzles(puzzles)

        LOGGER.info(f"--- Generating moveset complete---\n")

        return move_set

    def __convert_dict_to_puzzle(self, puzzle_info, sol, sub):
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

        # store the max length of the puzzle so that we need to find a solution better than..
        max_length = len(sub_solution)
        puzzle = PuzzleDTO(
            puzzle_id=puzzle_id,
            allowed_moves=self.__get_moves_for_puzzle(puzzle_info, sol),
            solution_state=sol.solution_state.split(";"),
            initial_state=sol.initial_state.split(";"),
            num_wildcards=sol.num_wildcards,
            submission_solution=sub_solution,
            max_moves=max_length,
        )

        return puzzle
