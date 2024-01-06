import logging
from abc import abstractmethod
from ast import literal_eval
from pathlib import Path

import pandas as pd

from src.conf import TrainConfig
from src.dtos.MovesetDTO import MovesetDTO
from src.dtos.PuzzleDTO import PuzzleDTO
from src.dtos.ResultDTO import ResultDTO
from src.dtos.ResultsDTO import ResultsDTO

LOGGER = logging.getLogger()


class MoveSetGeneratorBase:
    cfg: TrainConfig
    previous_results: ResultsDTO
    specific_puzzle: int
    puzzle_type: str
    movesetDTO: MovesetDTO

    def __init__(self, training_config: TrainConfig, resultsDTO: ResultsDTO | None):
        self.cfg = training_config
        self.specific_puzzle = self.cfg.config.specific_puzzle
        self.previous_results = resultsDTO  # type: ignore

        self.solution = pd.read_csv(Path(self.cfg.data.puzzles_file))
        self.submission = pd.read_csv(Path(self.cfg.data.submission_file))
        self.puzzle_info = pd.read_csv(
            Path(self.cfg.data.puzzles_info_file),
            index_col=self.cfg.data.puzzle_info_attributes.puzzle_info_puzzle_type_col_name,
        )
        self.puzzle_type = self.cfg.config.puzzle_type

    @abstractmethod
    def generate_moveset(self) -> MovesetDTO:
        pass

    def with_specific_puzzle(self, specific_puzzle):
        self.specific_puzzle = specific_puzzle

    def find_previous_specific_puzzle(self) -> ResultDTO:
        previous_result = None

        for result in self.previous_results.results:
            if result.puzzle_id == self.specific_puzzle:
                previous_result = result

        return previous_result  # type: ignore

    def to_csv(self, fname: str = "submission.csv"):
        puzzle_id = []
        puzzle_solution = []
        for puzzle in self.movesetDTO.puzzles:
            puzzle_id.append(puzzle.puzzle_id)
            puzzle_solution.append(puzzle.submission_solution)
        df = pd.DataFrame({"id": puzzle_id, "moves": puzzle_solution})
        df.to_csv(fname, index=False)

    def generate_puzzle(self, puzzle_id, puzzle_info, sol, sub_solution):
        # store the max length of the puzzle so that we need to find a solution better than..
        max_length = len(sub_solution)
        return PuzzleDTO(
            puzzle_id=puzzle_id,
            allowed_moves=self.__get_moves_for_puzzle(puzzle_info, sol),
            solution_state=sol.solution_state.split(";"),
            initial_state=sol.initial_state.split(";"),
            num_wildcards=sol.num_wildcards,
            submission_solution=sub_solution,
            max_moves=max_length,
        )

    def __get_moves_for_puzzle(self, puzzle_info, sol):
        allowed_moves = literal_eval(puzzle_info.loc[sol.puzzle_type, "allowed_moves"])
        # declare reverse moves
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
