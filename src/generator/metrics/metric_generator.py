"""Evaluation metric for Santa 2023."""

import logging
import pandas as pd
from ast import literal_eval
from sympy.combinatorics import Permutation

import datetime
from src.dtos import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.dtos.ResultDTO import ResultDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.exceptions.participant_visible_error import ParticipantVisibleError
from src.puzzles.puzzle_solver_base import PuzzleSolverBase
from src.reporter.metric_reporter import MetricsReporter

LOGGER = logging.getLogger()


class MetricGenerator:
    """
    generate the metrics for all the puzzles

    iterate over each puzzle and get the score, and any related stats of use.
    """

    results: ResultsDTO
    puzzle_solver: PuzzleSolverBase

    def __init__(self, puzzle_solver: PuzzleSolverBase):
        self.results = ResultsDTO()
        self.puzzle_solver = puzzle_solver

    def generate_score(self, ms: MovesetDTO) -> ResultsDTO:
        """
        iterate through all the puzzles and generate their score
        """
        self.__check_valid_data(ms)

        for sol, sub in zip(ms.solution.itertuples(), ms.submission.itertuples()):
            puzzle_score = (
                self.__generate_score_for_puzzle(ms.puzzle_info, sol, sub, ms.series_id_column_name, ms.moves_column_name))
            self.results.add_result(puzzle_score)

        return self.results

    def __check_valid_data(self, ms: MovesetDTO):
        if list(ms.submission.columns) != [ms.series_id_column_name, ms.moves_column_name]:
            raise ParticipantVisibleError(
                f"Submission must have columns {ms.series_id_column_name} and {ms.moves_column_name}."
            )
        return True

    def __generate_score_for_puzzle(self, puzzle_info, sol, sub, series_id_column_name, moves_column_name):
        puzzle_id = getattr(sol, series_id_column_name)
        assert puzzle_id == getattr(sub, series_id_column_name)

        # break out early if you dont want to wait for ages
        # if puzzle_id > 1:
        #     return ResultDTO(puzzle_id, 0.0, datetime.timedelta(0))

        puzzle = PuzzleDTO(
            puzzle_id=puzzle_id,
            allowed_moves=self.__get_moves_for_puzzle(puzzle_info, sol),
            solution_state=sol.solution_state.split(";"),
            initial_state=sol.initial_state.split(";"),
            num_wildcards=sol.num_wildcards,
        )

        # setting up for future puzzle solvers
        start = datetime.datetime.now()
        puzzle_result = self.puzzle_solver.score_puzzle(puzzle, getattr(sub, moves_column_name))

        resultDTO = ResultDTO(puzzle_id, puzzle_result, (datetime.datetime.now() - start))
        MetricsReporter().report_metrics_for_result(resultDTO)

        return resultDTO

    def __get_moves_for_puzzle(self, puzzle_info, sol):
        allowed_moves = literal_eval(
            puzzle_info.loc[sol.puzzle_type, "allowed_moves"]
        )
        allowed_moves = {k: Permutation(v) for k, v in allowed_moves.items()}
        return allowed_moves