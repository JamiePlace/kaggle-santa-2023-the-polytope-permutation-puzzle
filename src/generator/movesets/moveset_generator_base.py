import logging
from typing import List

from src.conf import TrainConfig
from src.dtos import EvolutionResultsDTO, MovesetDTO, ResultsDTO

LOGGER = logging.getLogger()


class MoveSetGeneratorBase:
    cfg: TrainConfig
    previous_results: ResultsDTO

    def __init__(self, training_config: TrainConfig, resultsDTO: ResultsDTO):
        self.cfg = training_config
        self.previous_results = resultsDTO

    def generate_moveset(self) -> List[str] | MovesetDTO:
        return []
