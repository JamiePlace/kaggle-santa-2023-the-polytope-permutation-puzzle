import logging

from src.conf import TrainConfig
from src.dtos import ResultsDTO
from src.dtos.EvolutionResultsDTO import EvolutionResultsDTO

LOGGER = logging.getLogger()


class MoveSetGeneratorBase:
    cfg: TrainConfig
    previous_results: ResultsDTO

    def __init__(self, training_config: TrainConfig, resultsDTO: ResultsDTO):
        self.cfg = training_config
        self.previous_results = resultsDTO

    def generate_moveset(self):
        return []
