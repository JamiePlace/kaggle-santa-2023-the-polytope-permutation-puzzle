import logging
from pathlib import Path

import hydra  # type: ignore

from src.conf import TrainConfig
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.generator.metrics.metric_generator import MetricGenerator
from src.generator.movesets.simple_moveset_generator import \
    SimpleMoveSetGenerator, MoveSetGeneratorBase
from src.puzzles.puzzle_solver_base import PuzzleSolverBase
from src.puzzles.sample_puzzle_solver import SamplePuzzleSolver
from src.reporter.metric_reporter import MetricsReporter

LOGGER = logging.getLogger(Path(__file__).name)
PROJECT_NAME = "Santa-2023"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s:%(name)s - %(message)s",
)

@hydra.main(config_path="conf", config_name="train", version_base="1.2")
def main(cfg: TrainConfig):
    LOGGER.info(f"Project name: {PROJECT_NAME} \n")

    specific_puzzle = cfg.config.specific_puzzle
    # set up initial data
    moveset_generator: MoveSetGeneratorBase = SimpleMoveSetGenerator(cfg, None)
    # moveset_generator.movesetDTO.submission has the data we need to check for loops

    breakpoint()

    puzzle_solver: PuzzleSolverBase = SamplePuzzleSolver()
    metric_generator = MetricGenerator(puzzle_solver, specific_puzzle)
    resultsDTO: ResultsDTO = metric_generator.generate_score(moveset_generator.movesetDTO)
    LOGGER.info(f"--- Finished ---")

    return




if __name__ == "__main__":
    main()  # type: ignore
