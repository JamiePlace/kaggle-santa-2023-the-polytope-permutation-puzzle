import ast
import logging
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.conf import TrainConfig
from src.dtos.PuzzleDTO import PuzzleDTO

LOGGER = logging.getLogger(Path(__file__).name)


class PuzzleGenerator:
    puzzles: pd.DataFrame
    puzzle_info: pd.DataFrame
    solution: pd.DataFrame

    cfg: TrainConfig

    def __init__(self, cfg: TrainConfig):
        LOGGER.info(f"-- Initialising PuzzleGenerator --")
        self.cfg = cfg
        self.puzzles = pd.read_csv(Path(self.cfg.data.puzzles_file))
        self.puzzle_info = pd.read_csv(Path(self.cfg.data.puzzles_info_file))
        self.solution = pd.read_csv(Path(self.cfg.data.submission_file))
        if self.cfg.config.specific_puzzle is not None:
            self.puzzles = self.puzzles.loc[self.puzzles["id"] == self.cfg.config.specific_puzzle]
        if self.cfg.config.puzzle_type is not None:
            self.puzzles = self.puzzles.loc[
                self.puzzles["puzzle_type"].apply(lambda x: x.split("_")[0])
                == self.cfg.config.puzzle_type
            ]
            self.puzzle_info = self.puzzle_info.loc[
                self.puzzle_info["puzzle_type"].apply(lambda x: x.split("_")[0])
                == self.cfg.config.puzzle_type
            ]
        self.puzzle_info = self.puzzle_info.set_index("puzzle_type")

    def fetch(self, pid: Optional[int] = None) -> List[PuzzleDTO]:
        if self.cfg.config.specific_puzzle is not None:
            pid = self.cfg.config.specific_puzzle
        if pid is not None:
            return [self.__generate_puzzle(pid)]
        output = np.empty(shape=len(self.puzzles.id), dtype=PuzzleDTO)
        for i, _pid in (
            pbar := tqdm(
                enumerate(self.puzzles.id),
                desc="Generating Puzzles -1",
                total=len(self.puzzles.id),
            )
        ):
            pbar.set_description(f"Generating Puzzles: id - {_pid}")
            output[i] = self.__generate_puzzle(_pid)
        return output.tolist()

    def __generate_puzzle(self, pid: int) -> PuzzleDTO:
        ptype = self.puzzles.loc[pid, "puzzle_type"]
        puzzle = PuzzleDTO(
            pid=pid,
            ptype=ptype,
            allowed_moves=self.__get_moves_for_puzzle(pid),
            solution_state=self.puzzles.loc[pid, "solution_state"],
            initial_state=self.puzzles.loc[pid, "initial_state"],
            num_wildcards=self.puzzles.loc[pid, "num_wildcards"],
        )

        if self.cfg.config.init_moves:
            moves = self.solution.loc[self.solution["id"] == pid, "moves"].values[0]
            puzzle.apply_moves(moves)
        return puzzle

    def __get_moves_for_puzzle(self, pid: int):
        if pid not in self.puzzles.id.values:
            raise Exception(f"Invalid puzzle id {pid}")
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
