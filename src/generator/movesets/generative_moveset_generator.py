import logging
import pandas as pd

from pathlib import Path
from src.dtos.MovesetDTO import MovesetDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase

LOGGER = logging.getLogger()


class GenerativeMoveSetGenerator(MoveSetGeneratorBase):
    """
    the start of a class to take the previous result as an inptut to the next generation of movesets
    """

    def generate_moveset(self):
        solution = pd.read_csv(Path(self.cfg.dir.data_dir) / "puzzles.csv")
        submission = pd.read_csv(Path(self.cfg.dir.sub_dir) / "submission.csv")
        puzzle_path = str(Path(self.cfg.dir.data_dir) / "puzzle_info.csv")

        easy_moveset = MovesetDTO(solution, submission, puzzle_path)
        return easy_moveset
