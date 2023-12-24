"""Evaluation metric for Santa 2023."""

import logging

from src.dtos import EvolutionResultsDTO, ResultDTO, ResultsDTO

LOGGER = logging.getLogger()


class MetricsReporter:
    """
    log the results of a single run of a puzzle
    or log the results of the entire set...

    maybe this class can eventually report all results out to file so as to save the moveset...?
    """

    def report_metrics_for_result(self, resultDTO: ResultDTO):
        LOGGER.debug(f"Scoring puzzle: {resultDTO.puzzle_id}")
        LOGGER.debug(f"\t score: {resultDTO.score}")
        LOGGER.debug(f"\t solved?: {resultDTO.solved}")
        LOGGER.debug(f"\t time taken: {resultDTO.time_taken} \n")

    def report_metrics_for_results(self, resultsDTO: ResultsDTO):
        LOGGER.debug(f"Results: ")
        LOGGER.debug(f"\t total score: {resultsDTO.combined_score}")
        LOGGER.debug(f"\t total time: {resultsDTO.cumulative_time} \n")

    def report_metrics_for_generative_results(self, evolutionResultsDTO: EvolutionResultsDTO):
        LOGGER.debug(f"Generative overall results: ")
        LOGGER.debug(f"\t generations: {evolutionResultsDTO.iterations}")
        LOGGER.debug(f"\t total time: {evolutionResultsDTO.cumulative_time}")
        average_runtime = evolutionResultsDTO.cumulative_time / evolutionResultsDTO.iterations
        LOGGER.debug(f"\t average time per generation: {average_runtime} \n")
