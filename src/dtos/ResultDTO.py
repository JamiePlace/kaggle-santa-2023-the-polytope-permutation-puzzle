from dataclasses import dataclass
import datetime
import pandas as pd


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
