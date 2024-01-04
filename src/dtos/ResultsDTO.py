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
        self.pos = -1

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return self

    def __next__(self):
        self.pos += 1
        if self.pos < len(self.results):
            return self.results[self.pos]
        raise StopIteration

    def __getitem__(self, key):
        return self.results[key]

    def __str__(self):
        output = ""
        for result in self.results:
            output += f"Puzzle ID: {result.puzzle_id}, Solved: {result.solved}, Errors: {result.error_count}, Score: {result.score}\n"
        return output

    def add_result(self, resultDTO: ResultDTO):
        if resultDTO is not None:
            self.combined_score = self.combined_score + resultDTO.score
            self.results.append(resultDTO)
            self.cumulative_time += resultDTO.time_taken
