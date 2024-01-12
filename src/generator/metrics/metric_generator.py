"""Evaluation metric for Santa 2023."""

import logging
from typing import List
from tqdm import tqdm

from src.dtos.PuzzleDTO import PuzzleDTO
from src.generator.movesets.moveset_generator_base import MoveSetGeneratorBase
from src.exceptions.participant_visible_error import ParticipantVisibleError

LOGGER = logging.getLogger()


class MetricGenerator:
    """
    generate the metrics for all the puzzles

    iterate over each puzzle and get the score, and any related stats of use.
    """
    puzzles: List[PuzzleDTO]

    def __init__(self, moveset_generator: MoveSetGeneratorBase):
        self.puzzles = moveset_generator.puzzles
        self.score = 0

    def generate_score(self):
        """
        iterate through all the puzzles and generate their score
        """


        LOGGER.info(f"--- Generating metrics using MetricGenerator ---")
        for puzzle in tqdm(self.puzzles):
            self.score += len(puzzle.moves)
        return self.score
