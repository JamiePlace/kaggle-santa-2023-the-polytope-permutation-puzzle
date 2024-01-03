import logging
from ast import literal_eval

import pandas as pd
from sympy.combinatorics import Permutation

from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.utils import get_project_root

LOGGER = logging.getLogger()


class SimpleMoveSetGenerator(MoveSetGeneratorBase):
    """
    OOTB moveset generator taking moveset from file.
    """

    def generate_moveset(self):
        LOGGER.debug(f"--- Generating moveset using SimpleMoveSetGenerator ---")

        root = get_project_root()

        solution = pd.read_csv(root / self.cfg.data.puzzles_file)
        submission = pd.read_csv(root / self.cfg.data.submission_file)
        puzzle_info = pd.read_csv(root / self.cfg.data.puzzles_info_file,
                                  index_col=self.cfg.data.puzzle_info_attributes.puzzle_info_puzzle_type_col_name)

        move_set = MovesetDTO(solution, submission, puzzle_info)

        puzzles = []
        for sol, sub in zip(solution.itertuples(), submission.itertuples()):
            puzzle = self.__convert_dict_to_puzzle(puzzle_info,
                                                   sol,
                                                   sub)
            if puzzle is not None:
                puzzles.append(puzzle)

        move_set.set_puzzles(puzzles)

        LOGGER.debug(f"--- Generating moveset complete---\n")

        return move_set

    def __convert_dict_to_puzzle(self, puzzle_info, sol, sub):
        puzzle_id = int(getattr(sol, self.cfg.data.puzzle_attributes.puzzle_id_col_name))
        assert puzzle_id == int(getattr(sub, self.cfg.data.submission_attributes.submission_id_col_name))

        # break out early if you dont want to wait for ages
        if self.specific_puzzle is not None:
            if puzzle_id != self.specific_puzzle:
                return None

        sub_solution = getattr(sub, self.cfg.data.submission_attributes.submission_moves_col_name)

        # store the max length of the puzzle so that we need to find a solution better than..
        max_length = len(sub_solution)
        puzzle = PuzzleDTO(puzzle_id=puzzle_id,
                           allowed_moves=self.__get_moves_for_puzzle(puzzle_info, sol),
                           solution_state=sol.solution_state.split(";"),
                           initial_state=sol.initial_state.split(";"),
                           num_wildcards=sol.num_wildcards,
                           submission_solution=sub_solution,
                           max_moves=max_length)

        return puzzle

    def __get_moves_for_puzzle(self, puzzle_info, sol):
        allowed_moves = literal_eval(
            puzzle_info.loc[sol.puzzle_type, "allowed_moves"]
        )
        allowed_moves = {k: Permutation(v) for k, v in allowed_moves.items()}
        return allowed_moves
