import logging

import numpy as np
import pandas as pd

from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.generator.movesets.generative_moveset_generator import GenerativeMoveSetGenerator
from src.utilities.puzzle_utils import get_x_lowest_error_puzzle_results, get_random_move_from_list_of_allowed_moves
from src.utils import get_project_root

LOGGER = logging.getLogger()


class RandomGenerativeMoveSetGenerator(GenerativeMoveSetGenerator):
    """
    This is really only to be used for solving 1 specific puzzle, as we will be generating multiple movesets for the
    opne puzzle, and re running it for multiple generations

    so far ive played around with

    adding in a sub set of completely random move sets to keep things fresh if thats a thing...
    then
    iterate through and nab the best results, because if we modify them and mess them up then we're doomed to have to
    generate them again by chance... of course they could be culled at a later stage if somehting with a better score
    comes in
    and finally
    we randomly update x number of moves in one moveset/solution in the hope that it brings us closer...
    """

    def generate_moveset(self):
        LOGGER.debug(f"--- Generating moveset using RandomGenerativeMoveSetGenerator ---")

        root = get_project_root()
        solution = pd.read_csv(root / self.cfg.data.puzzles_file)
        submission = pd.read_csv(root / self.cfg.data.submission_file)
        puzzle_info = pd.read_csv(root / self.cfg.data.puzzles_info_file,
                                  index_col=self.cfg.data.puzzle_info_attributes.puzzle_info_puzzle_type_col_name)

        if self.specific_puzzle is None:
            raise Exception(
                "this moveset generator requires a specific puzzle id, update the yaml file or project inputs")

        move_set = MovesetDTO(solution, submission, puzzle_info)
        new_puzzles = self.generate_move_set_from_previous_results()
        move_set.set_puzzles(new_puzzles)

        LOGGER.debug(f"--- Generating moveset complete---\n")

        return move_set

    def generate_move_set_from_previous_results(self):
        new_puzzles = []
        num_modification = 100
        num_random = 500

        # make randomly generated moves
        for x in range(num_random):
            new_puzzle = self.generate_random_move()
            new_puzzles.append(new_puzzle)

        # store the top x% incase doing something to them fucks em up
        best_results = get_x_lowest_error_puzzle_results(self.previous_results.results,
                                                         len(self.previous_results.results) / 20)
        for res in best_results:
            new_puzzles.append(res.puzzle)

        # take the best last moves and tweak them
        for x in range(num_modification):
            new_puzzle = self.generate_new_move_from_old_move()
            new_puzzles.append(new_puzzle)

        return new_puzzles

    def generate_new_move_from_old_move(self):
        # take the top 5%, or make this an input..
        best_move_sets = get_x_lowest_error_puzzle_results(self.previous_results.results,
                                                           len(self.previous_results.results) / 20)
        pp = best_move_sets[np.random.randint(0, len(best_move_sets))].puzzle

        number_of_changes = 1
        # number_of_changes = np.random.randint(1, int(pp.max_moves/4))
        new_move = self.make_new_move_form_old(pp.allowed_moves, pp.submission_solution, number_of_changes)

        puzzle = PuzzleDTO(puzzle_id=self.specific_puzzle,
                           allowed_moves=pp.allowed_moves,
                           solution_state=pp.solution_state,
                           initial_state=pp.initial_state,
                           num_wildcards=pp.num_wildcards,
                           submission_solution=new_move,
                           max_moves=pp.max_moves)

        return puzzle

    def generate_random_move(self):
        best_move_sets = get_x_lowest_error_puzzle_results(self.previous_results.results, 1)
        pp = best_move_sets[0].puzzle

        # new_move_length = np.random.randint(1, 11)
        new_move_length = np.random.randint(1, pp.max_moves)
        new_move = self.make_new_random_move(pp.allowed_moves, new_move_length)

        puzzle = PuzzleDTO(puzzle_id=self.specific_puzzle,
                           allowed_moves=pp.allowed_moves,
                           solution_state=pp.solution_state,
                           initial_state=pp.initial_state,
                           num_wildcards=pp.num_wildcards,
                           submission_solution=new_move,
                           max_moves=pp.max_moves)

        return puzzle

    def make_new_move_form_old(self, allowed_moves, best_move, number_of_changes):
        # force a change
        new_move = best_move
        while new_move == best_move:
            split_move = best_move.split(".")
            new_move = self.change_random_move(allowed_moves, split_move, number_of_changes)
            new_move = '.'.join(new_move)

        return new_move

    def make_new_random_move(self, allowed_moves, move_length):
        new_move_list = []
        for x in range(move_length):
            new_move_list.append(get_random_move_from_list_of_allowed_moves(allowed_moves))
        new_move = '.'.join(new_move_list)

        return new_move

    def change_random_move(self, allowed_moves, move, number):
        changed_move = move

        for x in range(number):
            changed_move[np.random.randint(0, len(changed_move))] = get_random_move_from_list_of_allowed_moves(
                allowed_moves)

        # add or remove a move
        # every now and again remove a move to see if we can get something smaller
        rand_num = np.random.randint(0, 10)
        if rand_num == 1 & len(move) > 2:
            changed_move = move.pop(np.random.randint(0, len(move)))

        return changed_move
