import logging
import pandas as pd

from pathlib import Path
from src.dtos.MovesetDTO import MovesetDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.utils import get_project_root

LOGGER = logging.getLogger()


class SimpleMoveSetGenerator(MoveSetGeneratorBase):
    """
    OOTB movset generator taking moveset from file.
    """
    def generate_moveset(self):
        root = get_project_root()

        solution = pd.read_csv(root / "data/puzzles.csv")
        submission = pd.read_csv(root / "submission.csv")
        puzzle_path = pd.read_csv(root / "data/puzzle_info.csv", index_col="puzzle_type")

        moveset = MovesetDTO(solution, submission, puzzle_path)
        return moveset