import logging
from pathlib import Path

import hydra  # type: ignore

from src.conf import TrainConfig
from src.dtos.EvolutionResultsDTO import EvolutionResultsDTO
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.generator.metrics.metric_generator import MetricGenerator
from src.generator.movesets.generative_moveset_generator import GenerativeMoveSetGenerator
from src.generator.movesets.iterative_generative_moveset_generator import IterativeGenerativeMoveSetGenerator
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.generator.movesets.random_generative_moveset_generator import RandomGenerativeMoveSetGenerator
from src.generator.movesets.simple_moveset_generator import \
    SimpleMoveSetGenerator
from src.puzzles.face_puzzle_solver import FacePuzzleSolver
from src.puzzles.puzzle_solver_base import PuzzleSolverBase
from src.puzzles.sample_puzzle_solver import SamplePuzzleSolver
from src.reporter.metric_reporter import MetricsReporter

LOGGER = logging.getLogger(Path(__file__).name)
PROJECT_NAME = "Santa-2023"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s:%(name)s - %(message)s",
)


@hydra.main(config_path="conf", config_name="train", version_base="1.2")
def main(cfg: TrainConfig):
    LOGGER.info(f"Project name: {PROJECT_NAME} \n")

    logging.getLogger().setLevel(logging.INFO)

    generations = cfg.config.generations
    if generations is None or generations == 0:
        LOGGER.info(f"--- Running once ---\n")
        run_once(cfg)
    else:
        LOGGER.info(f"--- Running with generations ---\n")
        run_with_generations(cfg)

    LOGGER.info(f"--- Finished ---")

    return

def run_once(cfg: TrainConfig):
    specific_puzzle = cfg.config.specific_puzzle

    # set up initial data
    moveset_generator: MoveSetGeneratorBase = SimpleMoveSetGenerator(cfg, None)
    moveset_generator.with_specific_puzzle(specific_puzzle)
    movesetDTO: MovesetDTO = moveset_generator.generate_moveset()

    # run and score
    puzzle_solver: PuzzleSolverBase = SamplePuzzleSolver()
    metric_generator = MetricGenerator(puzzle_solver, specific_puzzle)
    resultsDTO: ResultsDTO = metric_generator.generate_score(movesetDTO, True)

    # log the resutls
    metrics_reporter = MetricsReporter()
    metrics_reporter.report_metrics_for_results(resultsDTO)


def run_with_generations(cfg: TrainConfig):
    specific_puzzle = cfg.config.specific_puzzle
    generations = cfg.config.generations

    # for now lets only run generative movesets with a single puzzle, as it take quite long as it is....
    if specific_puzzle is None:
        raise Exception("ERROR: generatice movesets require a specific puzzle.")

    # generating moves
    moveset_generator: MoveSetGeneratorBase = SimpleMoveSetGenerator(cfg, {})
    moveset_generator.with_specific_puzzle(specific_puzzle)

    # solve and score the puzzle
    puzzle_solver: PuzzleSolverBase = SamplePuzzleSolver()
    # puzzle_solver: PuzzleSolverBase = FacePuzzleSolver("d1")

    # generate metrics and log
    metric_generator = MetricGenerator(puzzle_solver, specific_puzzle)
    metrics_reporter = MetricsReporter()

    # set up initial moveset data
    movesetDTO: MovesetDTO = moveset_generator.generate_moveset()

    # store generation history
    generations_data: EvolutionResultsDTO = EvolutionResultsDTO(generations)

    # iterate and solve
    for x in range(generations):
        LOGGER.info(f"--- Generation: {x} ---\n")

        # score the move set
        resultsDTO: ResultsDTO = metric_generator.generate_score(movesetDTO)

        # store results for next generation
        generations_data.add_generation_result(resultsDTO)

        # log stats for this set of results
        # can get quite noisey so enable what you will, maybe the logging info/debug level can be set by config..
        # metrics_reporter.report_metrics_for_results(resultsDTO)

        # feed the generation results into generating the next moveset
        # moveset_generator = SimpleMoveSetGenerator(cfg, resultsDTO)
        # moveset_generator = GenerativeMoveSetGenerator(cfg, resultsDTO)
        # moveset_generator = RandomGenerativeMoveSetGenerator(cfg, resultsDTO)
        moveset_generator = IterativeGenerativeMoveSetGenerator(cfg, resultsDTO)
        moveset_generator.with_specific_puzzle(specific_puzzle)
        movesetDTO = moveset_generator.generate_moveset()

        if resultsDTO.results[0].solved:
            LOGGER.info(f"solution found")
            MetricsReporter().report_metrics_for_result(resultsDTO.results[0])
            LOGGER.info(f"\n")
            break

    LOGGER.info(f"--- generations complete  ---")
    metrics_reporter.report_metrics_for_generative_results(generations_data)
    metrics_reporter.report_metrics_for_generative_results_smallest_error(generations_data)


if __name__ == "__main__":
    main()  # type: ignore
