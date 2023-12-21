import logging
from pathlib import Path
import hydra

from src.conf import TrainConfig
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

    # maybe these can be defined by enuma and stored in the cfg, i.e passed in by yaml file
    logging.getLogger().setLevel(logging.DEBUG)
    moveset_generator: MoveSetGeneratorBase = SimpleMoveSetGenerator(cfg, {})
    puzzle_solver: PuzzleSolverBase = SamplePuzzleSolver()
    metric_generator = MetricGenerator(puzzle_solver)
    metrics_reporter = MetricsReporter()

    generations = 1

    # set up initial data
    movesetDTO = moveset_generator.generate_moveset()

    # iterate and solve
    for x in range(generations):
        # score the move set
        resultsDTO = metric_generator.generate_score(movesetDTO)
        metrics_reporter.report_metrics_for_results(resultsDTO)

        # feed the score into generating the next moveset
        moveset_generator = GenerativeMoveSetGenerator(cfg, resultsDTO)
        movesetDTO = moveset_generator.generate_moveset()
    return


if __name__ == "__main__":
    main()
