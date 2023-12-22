import logging
import pandas as pd

from pathlib import Path
from src.dtos.MovesetDTO import MovesetDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.utils import get_project_root

LOGGER = logging.getLogger()


class GenerativeMoveSetGenerator(MoveSetGeneratorBase):
    """
    the start of a class to take the previous result as an input to the next generation of movesets
    """

    def generate_moveset(self):
        root = get_project_root()

        solution = pd.read_csv(root / "data/puzzles.csv")
        submission = pd.read_csv(root / "submission.csv")
        puzzle_info = pd.read_csv(root / "data/puzzle_info.csv", index_col="puzzle_type")

        easy_moveset = MovesetDTO(solution, submission, puzzle_info)
        return easy_moveset
