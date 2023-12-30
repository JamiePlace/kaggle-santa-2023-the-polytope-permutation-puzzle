import logging

import pandas as pd

from src.conf import TrainConfig
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.utils import get_project_root

LOGGER = logging.getLogger()


class GenerativeMoveSetGenerator(MoveSetGeneratorBase):

    def __init__(self, cfg: TrainConfig, resultsDTO: ResultsDTO):
        super().__init__(cfg, resultsDTO)

    def generate_moveset(self) -> MovesetDTO:
        LOGGER.info(f"--- Generating moveset using GenerativeMoveSetGenerator ---")

        root = get_project_root()

        solution = pd.read_csv(root / self.cfg.data.puzzles_file)
        submission = pd.read_csv(root / self.cfg.data.submission_file)
        puzzle_info = pd.read_csv(root / self.cfg.data.puzzles_info_file,
                                  index_col=self.cfg.data.puzzle_info_attributes.puzzle_info_puzzle_type_col_name)

        if self.specific_puzzle is None:
            raise Exception("this requires a specific puzzle id, update the yaml file or project inputs")

        move_set = MovesetDTO(solution, submission, puzzle_info)

        new_puzzles = []
        for result in self.previous_results.results:
            new_puzzles.append(result.puzzle)
        move_set.set_puzzles(new_puzzles)

        LOGGER.info(f"--- Generating moveset complete---\n")

        return move_set
