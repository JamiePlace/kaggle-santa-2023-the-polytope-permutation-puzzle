import logging
from pathlib import Path
import hydra  # type: ignore

from src.conf import TrainConfig
from src.dtos import EvolutionResultsDTO, ResultsDTO, MovesetDTO
from src.dtos.EvolutionResultsDTO import EvolutionResultsDTO
from src.generator.metrics.metric_generator import MetricGenerator
from src.generator.movesets.generative_moveset_generator import GenerativeMoveSetGenerator
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.generator.movesets.simple_moveset_generator import SimpleMoveSetGenerator
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

    logging.getLogger().setLevel(logging.DEBUG)

    generations = cfg.config.generations
    specific_puzzle = cfg.config.specific_puzzle

    # maybe these can be defined by enums and stored in the cfg, i.e passed in by yaml file
    moveset_generator: MoveSetGeneratorBase = SimpleMoveSetGenerator(cfg, {})
    puzzle_solver: PuzzleSolverBase = SamplePuzzleSolver()
    metric_generator = MetricGenerator(puzzle_solver, specific_puzzle)
    metrics_reporter = MetricsReporter()

    # set up initial data
    movesetDTO: MovesetDTO = moveset_generator.generate_moveset()

    # generation history
    generations_data: EvolutionResultsDTO = EvolutionResultsDTO(generations)

    # iterate and solve
    for x in range(generations):
        LOGGER.debug(f"--- Generation: {x} ---\n")

        # score the move set
        resultsDTO: ResultsDTO = metric_generator.generate_score(movesetDTO)
        metrics_reporter.report_metrics_for_results(resultsDTO)
        generations_data.add_generation_result(resultsDTO)

        # feed the score into generating the next moveset
        moveset_generator = GenerativeMoveSetGenerator(cfg, resultsDTO)
        movesetDTO = moveset_generator.generate_moveset()

    metrics_reporter.report_metrics_for_generative_results(generations_data)

    return

if __name__ == "__main__":
    main()  # type: ignore
