import logging
from pathlib import Path

import hydra

from src.conf import TrainConfig
from src.generator.puzzle_generator import PuzzleGenerator
from src.generator.metrics.metric_generator import MetricGenerator
from src.generator.movesets.simple_moveset_generator import SimpleMoveSetGenerator
from src.generator.movesets.loop_removal_moveset_generator import LoopRemovalMovesetGenerator

LOGGER = logging.getLogger(Path(__file__).name)
PROJECT_NAME = "Santa-2023"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s:%(name)s - %(message)s",
)


@hydra.main(config_path="conf", config_name="train", version_base="1.2")
def main(cfg: TrainConfig):
    LOGGER.info(f"Project name: {PROJECT_NAME} \n")
    puzzle_generator = PuzzleGenerator(cfg)
    puzzles = puzzle_generator.fetch()
    # set up initial data
    simple_moveset_generator = SimpleMoveSetGenerator(cfg, puzzles)
    simple_metric = MetricGenerator(simple_moveset_generator)
    simple_score = simple_metric.generate_score()

    loop_removal_moveset_generator = LoopRemovalMovesetGenerator(cfg, puzzles)
    loop_removal_metric = MetricGenerator(loop_removal_moveset_generator)
    loop_removal_score = loop_removal_metric.generate_score()


    LOGGER.info(f"--- Results ---")
    LOGGER.info(f"Old Results: {simple_score}")
    LOGGER.info(f"New Results: {loop_removal_score}")
    LOGGER.info(f"--- Finished ---")
    
    if cfg.config.specific_puzzle is None and cfg.config.puzzle_type is None:
        loop_removal_moveset_generator.to_csv("submission.csv")

    return


if __name__ == "__main__":
    main()  # type: ignore
