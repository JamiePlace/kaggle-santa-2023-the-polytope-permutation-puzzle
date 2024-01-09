import logging
from pathlib import Path
from pandas._libs.hashtable import value_count
from rich import print
from collections import Counter
import numpy as np

import hydra

from src.conf import TrainConfig
from src.generator.puzzle_generator import PuzzleGenerator
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
    for puzzle in puzzles:
        print(puzzle.pid, puzzle.validate())
    return


if __name__ == "__main__":
    main()  # type: ignore
