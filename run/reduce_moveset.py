import logging
import pandas as pd
from pathlib import Path

import hydra

from src.conf import TrainConfig
from src.dtos.ResultsDTO import ResultsDTO
from src.generator.metrics.metric_generator import MetricGenerator
from src.generator.movesets.loop_removal_moveset_generator import \
    LoopRemovalMovesetGenerator
from src.generator.movesets.simple_moveset_generator import \
    SimpleMoveSetGenerator
from src.puzzles.sample_puzzle_solver import SamplePuzzleSolver

LOGGER = logging.getLogger(Path(__file__).name)
PROJECT_NAME = "Santa-2023"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s:%(name)s - %(message)s",
)


@hydra.main(config_path="conf", config_name="train", version_base="1.2")
def main(cfg: TrainConfig):
    LOGGER.info(f"Project name: {PROJECT_NAME} \n")
    # set up initial data
    simple_moveset_generator: SimpleMoveSetGenerator = SimpleMoveSetGenerator(cfg)
    loop_removal_moveset_generator: LoopRemovalMovesetGenerator = LoopRemovalMovesetGenerator(cfg)

    metric_generator = MetricGenerator(SamplePuzzleSolver())
    old_resultsDTO = metric_generator.generate_score(simple_moveset_generator.movesetDTO)
    new_resultsDTO = metric_generator.generate_score(loop_removal_moveset_generator.movesetDTO)

    LOGGER.info(f"--- Results ---")
    LOGGER.info(f"Old Results: {old_resultsDTO.score()}")
    LOGGER.info(f"New Results: {new_resultsDTO.score()}")
    LOGGER.info(f"--- Finished ---")
    
    loop_removal_moveset_generator.to_csv("new_submission.csv")

    return


if __name__ == "__main__":
    main()  # type: ignore
