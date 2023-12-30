import datetime
import logging

import numpy as np

from src.dtos.PuzzleDTO import PuzzleDTO
from src.dtos.ResultDTO import ResultDTO
from src.exceptions.participant_visible_error import ParticipantVisibleError

LOGGER = logging.getLogger()


class PuzzleSolverBase:
    def score_puzzle(self, puzzle: PuzzleDTO, sub_solution):
        """Score the solution to a permutation puzzle."""

        start = datetime.datetime.now()

        # Apply submitted sequence of moves to the initial state, from left to right
        moves = puzzle.submission_solution.split(".")
        state = puzzle.initial_state

        LOGGER.debug(f"Attempting to solve puzzle: {puzzle.puzzle_id}")
        LOGGER.debug(f"Puzzle: {puzzle.puzzle_id}")
        LOGGER.debug(f"wildcards allowed: \t{puzzle.num_wildcards}")
        LOGGER.debug(f"allowed moves: {list(puzzle.allowed_moves.keys())}")
        LOGGER.debug(f"testing moves: {moves}")

        LOGGER.debug(f"initial state: \t{state}")
        faces = self.cube_state_to_faces(state)
        LOGGER.debug(f"initial faces: \t{faces}")

        for m in moves:
            power = 1
            try:
                if m[0] == "-":
                    m = m[1:]
                    power = -1
            except:
                LOGGER.info(f"error cannot get element[0] of string: \t{m}")
                raise ParticipantVisibleError(
                    f"error cannot get element[0] of string: \t{m}"
                )
            try:
                p = puzzle.allowed_moves[m]
            except KeyError:
                raise ParticipantVisibleError(f"{m} is not an allowed move for {self.puzzle_id}.")
            state = (p ** power)(state)
            # trying out different ways to do the perm multiplication
            # state = self.__multiple_1__(p, power, state)
            # state = self.__multiple_2__(p, power, state)

        LOGGER.debug(f"end state: \t\t{state}")
        faces = self.cube_state_to_faces(state)
        LOGGER.debug(f"end state faces: \t{faces}")

        LOGGER.debug(f"solution state: \t{puzzle.solution_state}")
        faces = self.cube_state_to_faces(puzzle.solution_state)
        LOGGER.debug(f"end state faces: \t{faces} \n")

        # Check that submitted moves solve puzzle
        num_wrong_facelets = sum(not (s == t) for s, t in zip(puzzle.solution_state, state))

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

        resultDTO = ResultDTO(
            puzzle.puzzle_id,
            puzzle,
            len(moves),
            solved,
            (datetime.datetime.now() - start),
            num_wrong_facelets,
            state)

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

    def cube_state_to_faces(self, state):
        """Convert a state list to a dictionary of labeled faces."""
        n = int(np.sqrt(len(state) / 6))  # cube_n/n/n
        n2 = n ** 2
        labels = f"d{n - 1},f0,r0,f{n - 1},r{n - 1},d0".split(",")
        faces = {}
        for i, l in enumerate(labels):
            face = state[n2 * i: n2 * (i + 1)]
            faces[l] = np.asarray(face).reshape(n, n).tolist()
        return faces
