import logging
from abc import abstractmethod

from src.conf import TrainConfig
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.ResultDTO import ResultDTO
from src.dtos.ResultsDTO import ResultsDTO

LOGGER = logging.getLogger()


class MoveSetGeneratorBase:
    cfg: TrainConfig
    previous_results: ResultsDTO
    specific_puzzle: int

    def __init__(self, training_config: TrainConfig, resultsDTO: ResultsDTO | None):
        self.cfg = training_config
        self.previous_results = resultsDTO

    @abstractmethod
    def generate_moveset(self) -> MovesetDTO:
        pass

    def with_specific_puzzle(self, specific_puzzle):
        self.specific_puzzle = specific_puzzle

    def find_previous_specific_puzzle(self) -> ResultDTO:
        previous_result = None

        for result in self.previous_results.results:
            if result.puzzle_id == self.specific_puzzle:
                previous_result = result

        return previous_result
