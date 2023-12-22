from dataclasses import dataclass
# from typing import List
import datetime
from typing import List

from src.dtos.ResultsDTO import ResultsDTO


# from src.dtos import ResultDTO


class EvolutionResultsDTO:
    """
    results of running all puzzles
    """
    iterations: int
    cumulative_time: datetime.timedelta
    results: List[ResultsDTO]

    def __init__(self, iterations):
        self.iterations = iterations
        self.results = []
        self.cumulative_time = datetime.timedelta(0)

    def add_generation_result(self, resultsDTO: ResultsDTO):
        self.results.append(resultsDTO)
        self.cumulative_time += resultsDTO.cumulative_time