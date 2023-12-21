from dataclasses import dataclass
import datetime


@dataclass
class ResultDTO:
    """
    result of running a puzzle
    """
    puzzle_id: int
    score: float
    time_taken: datetime.timedelta
