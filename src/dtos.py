# from typing import List
import datetime
import logging
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd
from sympy.combinatorics import Permutation

LOGGER = logging.getLogger()


@dataclass
class MovesetDTO:
    """
    defines the data required to score a puzzle
    """

    solution: pd.DataFrame
    submission: pd.DataFrame
    puzzle_info: pd.DataFrame

    series_id_column_name: str
    moves_column_name: str

    def __init__(self, solution, submission, puzzle_info):
        self.solution = solution
        self.submission = submission
        self.puzzle_info = puzzle_info

        self.series_id_column_name = "id"
        self.moves_column_name = "moves"


@dataclass
class PuzzleDTO:
    """
    contains the necessary attributes about a given puzzle
    """

    puzzle_id: str
    allowed_moves: Dict[str, Permutation | List[str]]
    solution_state: List[str]
    initial_state: List[str]
    num_wildcards: int


@dataclass
class ResultDTO:
    """
    result of running a puzzle
    """

    puzzle_id: int
    score: float
    solved: bool
    time_taken: datetime.timedelta
    sub_solution: pd.DataFrame
    num_wrong_facelets: int
    end_state: List[str]


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
        self.combined_score = self.combined_score + resultDTO.score
        self.results.append(resultDTO)
        self.cumulative_time += resultDTO.time_taken


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
