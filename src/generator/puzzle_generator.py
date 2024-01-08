import logging
import ast
from pathlib import Path
from typing import List,Optional

import pandas as pd
import numpy as np

from src.conf import TrainConfig
from src.dtos.PuzzleDTO import PuzzleDTO

LOGGER = logging.getLogger(Path(__file__).name)

class PuzzleGenerator:
    puzzles: pd.DataFrame
    puzzle_info: pd.DataFrame

    cfg: TrainConfig

    def __init__(self, cfg: TrainConfig):
        LOGGER.info(f"-- Initialising PuzzleGenerator --")
        self.cfg = cfg
        self.puzzles = pd.read_csv(Path(self.cfg.data.puzzles_file))
        self.puzzle_info = pd.read_csv(
            Path(self.cfg.data.puzzles_info_file),
            index_col=self.cfg.data.puzzle_info_attributes.puzzle_info_puzzle_type_col_name,
        )

    def fetch(self, pid: Optional[int] = None) -> List[PuzzleDTO]:
        if pid is not None:
            return [self.__generate_puzzle(pid)]
        output = np.empty(shape=len(self.puzzles.id), dtype=PuzzleDTO)
        for i,_pid in enumerate(self.puzzles.id):
            output[i] = self.__generate_puzzle(_pid)
        return output.tolist()

    def __generate_puzzle(self, pid: int) -> PuzzleDTO:
        # store the max length of the puzzle so that we need to find a solution better than..
        return PuzzleDTO(
            pid=pid,
            allowed_moves=self.__get_moves_for_puzzle(pid),
            solution_state=self.puzzles.loc[pid, "solution_state"],
            initial_state=self.puzzles.loc[pid, "initial_state"],
            num_wildcards=self.puzzles.loc[pid, "num_wildcards"],
            submission_solution="",
            max_moves=len(self.puzzles.loc[pid, "initial_state"]),
        )

    def __get_moves_for_puzzle(self,pid: int):
        puzzle_type = self.puzzles.loc[pid, "puzzle_type"]
        allowed_moves = ast.literal_eval(self.puzzle_info.loc[puzzle_type, "allowed_moves"])
        allowed_moves = self.__init_reverse_moves(allowed_moves)
        return allowed_moves

    def __init_reverse_moves(self, moves):
        new_moves = {}
        for m in moves.keys():
            new_moves[m] = moves[m]
            xform = moves[m]
            m_inv = "-" + m
            xform_inv = len(xform) * [0]
            for i in range(len(xform)):
                xform_inv[xform[i]] = i
            new_moves[m_inv] = xform_inv
        return new_moves
