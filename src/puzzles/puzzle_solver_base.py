import datetime
import logging

import numpy as np

from src.dtos.PuzzleDTO import PuzzleDTO
from src.dtos.PuzzleStateChangeDTO import PuzzleStateChangeDTO
from src.dtos.ResultDTO import ResultDTO
from src.exceptions.participant_visible_error import ParticipantVisibleError

LOGGER = logging.getLogger()


class PuzzleSolverBase:
    def get_scoring_method(self, solution, end_state):
        return sum(not (s == t) for s, t in zip(solution, end_state))

    def is_puzzle_solved(self, num_wrong_facelets, num_wildcards):
        solved: bool
        if num_wrong_facelets > num_wildcards:
            solved = False
        else:
            solved = True
        return solved

    def score_puzzle(self, puzzle: PuzzleDTO, validate = False):
        """Score the solution to a permutation puzzle."""

        start = datetime.datetime.now()

        # Apply submitted sequence of moves to the initial state, from left to right
        moves = puzzle.submission_solution.split(".")
        state = puzzle.initial_state
        allowed_moves = puzzle.allowed_moves

        LOGGER.debug(f"Attempting to solve puzzle: {puzzle.puzzle_id}")
        LOGGER.debug(f"Puzzle: {puzzle.puzzle_id}")
        LOGGER.debug(f"wildcards allowed: \t{puzzle.num_wildcards}")
        LOGGER.debug(f"allowed moves: {list(puzzle.allowed_moves.keys())}")
        LOGGER.debug(f"testing moves: {moves}")

        LOGGER.debug(f"initial state: \t{state}")
        faces = self.cube_state_to_faces(state)
        LOGGER.debug(f"initial faces: \t{faces}")

        move_to_error_mapping = []
        # for m in moves:
        #    power = 1
        #    try:
        #        if m[0] == "-":
        #            m = m[1:]
        #            power = -1
        #    except:
        #        LOGGER.info(f"error cannot get element[0] of string: \t{m}")
        #        raise ParticipantVisibleError(
        #            f"error cannot get element[0] of string: \t{m}"
        #        )
        #    try:
        #        p = puzzle.allowed_moves[m]
        #    except KeyError:
        #        raise ParticipantVisibleError(f"{m} is not an allowed move for {puzzle.puzzle_id}.")
        #    state = (p ** power)(state)
        #    num_wrong_facelets = sum(s != t for s, t in zip(puzzle.solution_state, state))
        #    move_to_error_mapping.append(num_wrong_facelets)
        for m in moves:
            state = self.apply_move(allowed_moves, m, state)
            num_wrong_facelets = sum(s != t for s, t in zip(puzzle.solution_state, state))
            move_to_error_mapping.append(num_wrong_facelets)

        LOGGER.debug(f"end state: \t\t{state}")
        faces = self.cube_state_to_faces(state)
        LOGGER.debug(f"end state faces: \t{faces}")

        LOGGER.debug(f"solution state: \t{puzzle.solution_state}")
        faces = self.cube_state_to_faces(puzzle.solution_state)
        LOGGER.debug(f"end state faces: \t{faces} \n")

        # Check that submitted moves solve puzzle
        # get the number of wrong tiles so we can check how close the solution is
        # num_wrong_facelets = sum(not (s == t) for s, t in zip(puzzle.solution_state, state))
        num_wrong_facelets = self.get_scoring_method(puzzle.solution_state, state)
        num_wrong_facelets = sum(s != t for s, t in zip(puzzle.solution_state, state))

        solved = self.is_puzzle_solved(num_wrong_facelets, puzzle.num_wildcards)

        if not solved:
            raise ParticipantVisibleError(f"your solution does not solve the puzzle.")

        if validate:
            return True


        attempt = 0
        previous_error = num_wrong_facelets
        previous_error_mapping = move_to_error_mapping
        if puzzle.previous_state is not None:
            attempt = puzzle.previous_state.attempt + 1
            previous_error = puzzle.previous_state.error_count
            previous_error_mapping = puzzle.previous_state.move_to_error_mapping

        # store the previous state
        previous_state = PuzzleStateChangeDTO(
            puzzle_id=puzzle.puzzle_id,
            initial_state=puzzle.initial_state,
            after_state=state,
            solution_used=puzzle.submission_solution,
            error_count=previous_error,
            move_to_error_mapping=previous_error_mapping,
            attempt=attempt,
        )
        # for now store the previous state in the puzzle as we only have access to the puzzle on the scoring class here
        # we create the result here so we don't have anything to draw of to get the previous result, unless we pass in
        # the result object instead of the puzzle object
        puzzle.previous_state = previous_state

        # setup a result for this puzzle
        resultDTO = ResultDTO(
            puzzle_id=puzzle.puzzle_id,
            puzzle=puzzle,
            score=len(moves),
            solved=solved,
            time_taken=(datetime.datetime.now() - start),
            end_state=state,
            error_count=num_wrong_facelets,
            move_to_error_mapping=move_to_error_mapping,
        )

        return resultDTO

    def cube_state_to_faces(self, state):
        """Convert a state list to a dictionary of labeled faces."""
        n = int(np.sqrt(len(state) / 6))  # cube_n/n/n
        n2 = n**2
        labels = f"d{n - 1},f0,r0,f{n - 1},r{n - 1},d0".split(",")
        faces = {}
        for i, l in enumerate(labels):
            face = state[n2 * i : n2 * (i + 1)]
            faces[l] = np.asarray(face).reshape(n, n).tolist()
        return faces

    def apply_move(self, moves, move, state):
        m = move

        move_list = moves[m]
        state = np.array(state)[move_list]

        return state.tolist()
