import datetime
from dataclasses import dataclass
from typing import List

from src.dtos.ResultDTO import ResultDTO


@dataclass
class ResultsDTO:
    """
    results of running all puzzles
    """

    combined_score: float
    cumulative_time: datetime.timedelta
    results: List[ResultDTO]

    def __init__(self):
        self.combined_score = 0.0
        self.results = []
        self.cumulative_time = datetime.timedelta(0)

    def add_result(self, resultDTO: ResultDTO):
        if resultDTO is not None:
            self.combined_score = self.combined_score + resultDTO.score
            self.results.append(resultDTO)
            self.cumulative_time += resultDTO.time_taken
