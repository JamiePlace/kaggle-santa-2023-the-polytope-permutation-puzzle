"""Evaluation metric for Santa 2023."""

import logging
from typing import Optional
from tqdm import tqdm

from src.dtos.MovesetDTO import MovesetDTO
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

    puzzle_solver: PuzzleSolverBase
    specific_puzzle: Optional[int]

    def __init__(self, puzzle_solver: PuzzleSolverBase, specific_puzzle: Optional[int] = None):
        self.puzzle_solver = puzzle_solver
        self.specific_puzzle = specific_puzzle

    def generate_score(self, ms: MovesetDTO, print=False, exit_if_solution_found=False) -> ResultsDTO:
        """
        iterate through all the puzzles and generate their score
        """
        self.__check_valid_data(ms)

        results = ResultsDTO()

        LOGGER.info(f"--- Generating metrics using MetricGenerator ---")
        for puzzle in tqdm(ms.puzzles):
            resultDTO = self.puzzle_solver.score_puzzle(puzzle, puzzle.submission_solution)
            if print:
                MetricsReporter().report_metrics_for_result(resultDTO)
            results.add_result(resultDTO)

            if exit_if_solution_found and resultDTO.solved:
                results.results = [resultDTO]
                return results

        return results

    def __check_valid_data(self, ms: MovesetDTO):
        if list(ms.submission.columns) != [ms.series_id_column_name, ms.moves_column_name]:
            raise ParticipantVisibleError(
                f"Submission must have columns {ms.series_id_column_name} and {ms.moves_column_name}."
            )
        return True
