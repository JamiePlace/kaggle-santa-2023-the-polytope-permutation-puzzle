import logging
from pathlib import Path
from rich import print

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
    puzzles = puzzle_generator.fetch(0)
    print(puzzles[0])
    puzzles[0].apply_move("r1")
    puzzles[0].apply_move("-f1")
    print(puzzles[0])
    print(puzzles[0].previous_states)
    return


if __name__ == "__main__":
    main()  # type: ignore
