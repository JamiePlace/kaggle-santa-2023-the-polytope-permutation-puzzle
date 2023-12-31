"""Evaluation metric for Santa 2023."""

import logging

from src.dtos.EvolutionResultsDTO import EvolutionResultsDTO
from src.dtos.ResultDTO import ResultDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.utilities.puzzle_utils import get_number_of_moves_for_puzzle, is_puzzle_solution_same

LOGGER = logging.getLogger()


class MetricsReporter:
    """
    log the results of a single run of a puzzle
    or log the results of the entire set...

    maybe this class can eventually report all results out to file so as to save the moveset...?
    """

    def report_metrics_for_result(self, resultDTO: ResultDTO):
        LOGGER.info(f"Scoring puzzle: {resultDTO.puzzle_id}")
        LOGGER.info(f"\t score: {resultDTO.score}")
        LOGGER.info(f"\t solved?: {resultDTO.solved}")
        if resultDTO.num_wrong_facelets > 0:
            LOGGER.info(f"\t number incorrect: {resultDTO.num_wrong_facelets}")
        LOGGER.info(f"\t time taken: {resultDTO.time_taken} \n")

    def report_metrics_for_results(self, resultsDTO: ResultsDTO):
        LOGGER.info(f"Results: ")
        LOGGER.info(f"\t total score: {resultsDTO.combined_score}")
        LOGGER.info(f"\t total time: {resultsDTO.cumulative_time} \n")

    def report_puzzle_stats_largest_score(self, resultsDTO: ResultsDTO):
        topx = 10
        largest_scores = []
        for puzzle in resultsDTO.results:
            if len(largest_scores) < topx:
                largest_scores.append(puzzle)
            else:
                for index, top_x_puzzle in enumerate(largest_scores):
                    if puzzle.score > top_x_puzzle.score:
                        largest_scores[index] = top_x_puzzle
                        break

        LOGGER.info(f"Puzzle stats: puzzles with largest moves")
        for index, score in enumerate(largest_scores):
            LOGGER.info(f"\t\t puzzle id: {score.puzzle_id} \tscore: {score.score}")
        LOGGER.info(f"\n")

    def report_puzzle_stats_largest_time(self, resultsDTO: ResultsDTO):
        topx = 10
        largest_times = []
        for puzzle in resultsDTO.results:
            if len(largest_times) < topx:
                largest_times.append(puzzle)
            else:
                for index, top_x_puzzle in enumerate(largest_times):
                    if puzzle.time_taken < top_x_puzzle.time_taken:
                        if len(puzzle.puzzle.submission_solution) < len(top_x_puzzle.puzzle.submission_solution):
                            largest_times[index] = puzzle
                            break

        largest_times.sort(key=lambda x: x.time_taken, reverse=True)

        LOGGER.info(f"Puzzle stats: puzzles with smallest error (number of incorrect values)")
        for index, largest_time in enumerate(largest_times):
            LOGGER.info(f"\t\t puzzle id: {largest_time.puzzle_id} \ttime: {largest_time.time_taken}")
        LOGGER.info(f"\n")

    def report_puzzle_stats_smallest_error(self, resultsDTO: ResultsDTO):
        topx = 10
        best_scores = []
        for puzzle in resultsDTO.results:
            if len(best_scores) < topx:
                best_scores.append(puzzle)
            else:
                for index, top_x_puzzle in enumerate(best_scores):
                    if puzzle.num_wrong_facelets < top_x_puzzle.num_wrong_facelets:
                        if (get_number_of_moves_for_puzzle(puzzle.puzzle) <
                                get_number_of_moves_for_puzzle(top_x_puzzle.puzzle)):
                            best_scores[index] = puzzle
                            break

        best_scores.sort(key=lambda x: x.num_wrong_facelets, reverse=True)

        LOGGER.info(f"Puzzle stats: puzzles with smallest error (number of incorrect values)")
        for index, score in enumerate(best_scores):
            LOGGER.info(
                f"\t\t puzzle id: {score.puzzle_id} \terrors: {score.num_wrong_facelets} \t puzzle solution: {score.puzzle.submission_solution}")
        LOGGER.info(f"\n")

    def report_metrics_for_generative_results(self, evolutionResultsDTO: EvolutionResultsDTO):
        LOGGER.info(f"Generative overall results: ")
        LOGGER.info(f"\t generations: {evolutionResultsDTO.iterations}")
        LOGGER.info(f"\t total time: {evolutionResultsDTO.cumulative_time}")
        average_runtime = evolutionResultsDTO.cumulative_time / evolutionResultsDTO.iterations
        LOGGER.info(f"\t average time per generation: {average_runtime} \n")

    def report_metrics_for_generative_results_smallest_error(self, evolutionResultsDTO: EvolutionResultsDTO):
        topx = 10
        best_scores = []
        for gen_result in evolutionResultsDTO.results:
            for gen_result_puzzle in gen_result.results:
                if len(best_scores) < topx:
                    # init the array
                    best_scores.append(gen_result_puzzle)
                    best_scores.sort(key=lambda x: x.num_wrong_facelets, reverse=True)
                else:
                    # check array of scores to see can we add it
                    for index, top_x_puzzle in enumerate(best_scores):
                        # make sure it hasnt been added by any other generation
                        if not is_puzzle_solution_same(gen_result_puzzle.puzzle, top_x_puzzle.puzzle):
                            if gen_result_puzzle.num_wrong_facelets < top_x_puzzle.num_wrong_facelets:
                                best_scores[index] = gen_result_puzzle
                                break
                            else:
                                if ((gen_result_puzzle.num_wrong_facelets == top_x_puzzle.num_wrong_facelets) &
                                        (get_number_of_moves_for_puzzle(gen_result_puzzle.puzzle) <
                                         get_number_of_moves_for_puzzle(top_x_puzzle.puzzle))):
                                    best_scores[index] = gen_result_puzzle
                                    break

        best_scores.sort(key=lambda x: x.num_wrong_facelets, reverse=True)

        LOGGER.info(f"Puzzle stats: puzzles with smallest error (number of incorrect values)")
        for index, score in enumerate(best_scores):
            LOGGER.info(
                f"\t\t puzzle id: {score.puzzle_id} \tsolved: {score.solved} \terrors: {score.num_wrong_facelets} \t puzzle solution: {score.puzzle.submission_solution}")
        LOGGER.info(f"\n")
