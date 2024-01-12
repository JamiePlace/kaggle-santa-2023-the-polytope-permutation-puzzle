import logging
from typing import Optional, List

from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.dtos.ResultsDTO import ResultsDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase

LOGGER = logging.getLogger()


class SimpleMoveSetGenerator(MoveSetGeneratorBase):
    """
    OOTB moveset generator taking moveset from file.
    """

    movesetDTO: MovesetDTO
    solutions: dict
    puzzle_type: str
    specific_puzzle: int
    puzzles: List[PuzzleDTO]

    def __init__(self, cfg, puzzles: List[PuzzleDTO]):
        super().__init__(cfg)
        self.puzzles = puzzles
