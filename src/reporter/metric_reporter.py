"""Evaluation metric for Santa 2023."""

import logging

from src.dtos import ResultsDTO, ResultDTO

LOGGER = logging.getLogger()


class MetricsReporter:
    """
    log the results of a single run of a puzzle
    or log the results of the entire set...
    """

    def report_metrics_for_result(self, resultDTO: ResultDTO):
        LOGGER.debug(f"Scoring puzzle: {resultDTO.puzzle_id}")
        LOGGER.debug(f"\t score: {resultDTO.score}")
        LOGGER.debug(f"\t time taken: {resultDTO.time_taken} \n")

    def report_metrics_for_results(self, resultsDTO: ResultsDTO):
        LOGGER.debug(f"Results: ")
        LOGGER.debug(f"\t total score: {resultsDTO.combined_score}")
        LOGGER.debug(f"\t total time: {resultsDTO.cumulative_time} \n")
