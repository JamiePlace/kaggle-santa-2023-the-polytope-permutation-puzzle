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
        LOGGER.debug(f"--- Generating moveset using GenerativeMoveSetGenerator ---")
        if self.specific_puzzle is None:
            raise Exception("this requires a specific puzzle id, update the yaml file or project inputs")

        move_set = MovesetDTO(self.solution, self.submission, self.puzzle_info)

        new_puzzles = []
        for result in self.previous_results.results:
            new_puzzles.append(result.puzzle)
        move_set.set_puzzles(new_puzzles)

        LOGGER.debug(f"--- Generating moveset complete---\n")

        return move_set
