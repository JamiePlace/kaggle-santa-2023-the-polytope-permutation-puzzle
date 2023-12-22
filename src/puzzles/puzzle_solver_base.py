import logging
import datetime

import numpy as np

from src.dtos.ResultDTO import ResultDTO
from src.exceptions.participant_visible_error import ParticipantVisibleError

LOGGER = logging.getLogger()


class PuzzleSolverBase:

    def score_puzzle(self, puzzle, sub_solution):
        """Score the solution to a permutation puzzle."""

        start = datetime.datetime.now()

        # Apply submitted sequence of moves to the initial state, from left to right
        moves = sub_solution.split(".")
        state = puzzle.initial_state

        LOGGER.debug(f"Attempting to solve puzzle: {puzzle.puzzle_id}")
        LOGGER.debug(f"Puzzle: {puzzle.puzzle_id}")
        LOGGER.debug(f"initial state: \t{state}")
        LOGGER.debug(f"solution state: \t{puzzle.solution_state}")
        LOGGER.debug(f"wildcards allowed: {puzzle.num_wildcards}")
        LOGGER.debug(f"allowed moves: {list(puzzle.allowed_moves.keys())}")
        LOGGER.debug(f"testing moves: {moves} \n")


        for m in moves:
            power = 1
            if m[0] == "-":
                m = m[1:]
                power = -1
            try:
                p = puzzle.allowed_moves[m]
            except KeyError:
                raise ParticipantVisibleError(
                    f"{m} is not an allowed move for {self.puzzle_id}."
                )
            state = (p ** power)(state)
            # state = self.__multiple_1__(p, power, state)
            # state = self.__multiple_2__(p, power, state)

        # Check that submitted moves solve puzzle
        num_wrong_facelets = sum(
            not (s == t) for s, t in zip(puzzle.solution_state, state)
        )

        solved: bool
        if num_wrong_facelets > puzzle.num_wildcards:
            solved = False
            # for now do not raise an error, as we would probably like to create some sort of feedback loop into the
            # next iteration

            # raise ParticipantVisibleError(
            #     f"Submitted moves do not solve {self.puzzle_id}."
            # )
        else:
            solved = True

        resultDTO = ResultDTO(puzzle.puzzle_id,
                              len(moves),
                              solved,
                              (datetime.datetime.now() - start),
                              sub_solution,
                              num_wrong_facelets)

        return resultDTO


    def __multiple_1__(self, permutation, power, state):
        # LOGGER.debug(f"permutation : {permutation.array_form} ")
        # LOGGER.debug(f"before state : {state} ")
        new_state = (permutation ** power)(state)
        # LOGGER.debug(f"after state : {new_state} \n")
        return new_state

    def __multiple_2__(self, permutation, power, state):

        LOGGER.debug(f"permutation : {permutation.array_form} ")
        LOGGER.debug(f"before state : {state} ")
        new_state = np.matmul((permutation ** power), state)
        LOGGER.debug(f"after state : {new_state} \n")

        return new_state
