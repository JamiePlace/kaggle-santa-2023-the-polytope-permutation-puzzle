import logging


from src.exceptions.participant_visible_error import ParticipantVisibleError

LOGGER = logging.getLogger()


class PuzzleSolverBase:

    def score_puzzle(self, puzzle, sub_solution):
        """Score the solution to a permutation puzzle."""
        # Apply submitted sequence of moves to the initial state, from left to right
        moves = sub_solution.split(".")
        state = puzzle.initial_state
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

        # Check that submitted moves solve puzzle
        num_wrong_facelets = sum(
            not (s == t) for s, t in zip(puzzle.solution_state, state)
        )
        if num_wrong_facelets > puzzle.num_wildcards:
            raise ParticipantVisibleError(
                f"Submitted moves do not solve {self.puzzle_id}."
            )

        return len(moves)
