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

        # todo bring the yaml config values back in
        solution = pd.read_csv(root / "data/puzzles.csv")
        submission = pd.read_csv(root / "submission.csv")
        puzzle_info = pd.read_csv(root / "data/puzzle_info.csv", index_col="puzzle_type")

        easy_moveset = MovesetDTO(solution, submission, puzzle_info)
        return easy_moveset



"""
submission is the ceiling of the moveset size

{x1, x2, x3...... xX  } length Y

new moveset
[
    {x1, x2, x3...... xX  } length Y
    .
    .
    .
    .
    {x1, x2, x3...... xX  } length (y-some value)
]

take the submission, lets say 100 elements in array
break it up into secitons of 5/10 etc and then randomly move them around to create a new moveset

we can still add some sense of randomnes by either changing one or more values in a move 

or we can entirely generate a full move randomly and fire it into the moveset and hope for the best...
"""