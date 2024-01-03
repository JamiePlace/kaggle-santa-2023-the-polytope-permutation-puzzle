import logging

import numpy as np
import pandas as pd

from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.dtos.PuzzleStateChangeDTO import PuzzleStateChangeDTO
from src.generator.movesets.generative_moveset_generator import GenerativeMoveSetGenerator
from src.utilities.puzzle_utils import get_number_of_moves_for_puzzle, is_puzzle_solution_same, \
    get_random_move_from_list_of_allowed_moves, get_x_lowest_error_puzzle_results

LOGGER = logging.getLogger()


class AtomicMoveSetGenerator(GenerativeMoveSetGenerator):
    """
    small af
    """
    def __init__(self, cfg, resultsDTO):
        super().__init__(cfg, resultsDTO)

    def generate_moveset(self):
        LOGGER.debug(f"--- Generating moveset using IterativeGenerativeMoveSetGenerator ---")
        if self.specific_puzzle is None:
            raise Exception(
                "this moveset generator requires a specific puzzle id, update the yaml file or project inputs")

        move_set = MovesetDTO(self.solution, self.submission, self.puzzle_info)
        new_puzzles = self.generate_move_set_from_previous_results()
        move_set.set_puzzles(new_puzzles)

        LOGGER.debug(f"--- Generating moveset complete---\n")

        return move_set

    def generate_move_set_from_previous_results(self):
        new_puzzles = []
        max_len_solution = 2000
        max_moves = 100

        pr = self.previous_results.results

        best_move_sets = []
        if len(self.previous_results.results) == 1:
            best_move_sets = self.previous_results.results
        else:
            # get the top x% of results and reuse them for 80% of the next new moveset
            # then we will fill the last 20% with random new stuff to bring in more variety
            for x in range(9):
                best_move_sets = best_move_sets + get_x_lowest_error_puzzle_results(pr, len(pr) / 10)

        # take the best last moves and tweak them
        # for result in self.previous_results.results:
        for result in best_move_sets:
            new_puzzle = self.generate_new_move_from_old_move(result)
            # check solution length, if too long cull it
            if len(new_puzzle.submission_solution) < max_len_solution:
                new_puzzles.append(new_puzzle)

        # # make randomly generated moves
        # only add more moves if we have space, otherwise wait for the culling to help
        while len(new_puzzles) < max_moves:
            new_puzzle = self.generate_random_move(2)
            new_puzzles.append(new_puzzle)

        return new_puzzles

    def generate_new_move_from_old_move(self, result):
        pp = result.puzzle
        previous_state: PuzzleStateChangeDTO = pp.previous_state

        previous_error = previous_state.error_count
        recent_error = result.error_count
        if recent_error > previous_error:
            # change up the move to find a better move
            old_move = pp.submission_solution
            split_move = old_move.split(".")

            if previous_state.attempt < 10:
                # allow it to run the score higher as a subsequent move could bring it back down
                split_move.append(get_random_move_from_list_of_allowed_moves(pp.allowed_moves))
            else:
                split_move[(len(split_move) - 1)] = get_random_move_from_list_of_allowed_moves(pp.allowed_moves)

            # or just comment out above if else, and just change a value and nevermind the attempt stuff...
            # split_move[(len(split_move) - 1)] = get_random_move_from_list_of_allowed_moves(pp.allowed_moves)

            new_move = '.'.join(split_move)
            previous_state.attempt = previous_state.attempt + 1
        else:
            # we have an improvement, add a new move
            old_move = pp.submission_solution
            split_move = old_move.split(".")
            split_move.append(get_random_move_from_list_of_allowed_moves(pp.allowed_moves))
            new_move = '.'.join(split_move)
            previous_state.attempt = 0

        puzzle = PuzzleDTO(puzzle_id=self.specific_puzzle,
                           allowed_moves=pp.allowed_moves,
                           solution_state=pp.solution_state,
                           initial_state=pp.initial_state,
                           num_wildcards=pp.num_wildcards,
                           submission_solution=new_move,
                           max_moves=pp.max_moves)

        return puzzle

    def generate_random_move(self, move_length):
        # get hold of any puzzle
        # it doesn't matter which as generative moveset generators only work with 1 puzzle...
        best_move_sets = get_x_lowest_error_puzzle_results(self.previous_results.results, 1)
        pp = best_move_sets[0].puzzle

        new_move_length = np.random.randint(1, move_length)
        new_move = self.make_new_random_move(pp.allowed_moves, new_move_length)

        puzzle = PuzzleDTO(puzzle_id=self.specific_puzzle,
                           allowed_moves=pp.allowed_moves,
                           solution_state=pp.solution_state,
                           initial_state=pp.initial_state,
                           num_wildcards=pp.num_wildcards,
                           submission_solution=new_move,
                           max_moves=pp.max_moves)

        return puzzle

    def make_new_random_move(self, allowed_moves, move_length):
        new_move_list = []
        for _ in range(move_length):
            new_move_list.append(get_random_move_from_list_of_allowed_moves(allowed_moves))
        new_move = '.'.join(new_move_list)

        return new_move
