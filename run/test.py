import numpy as np
import pandas as pd
from hydra import compose, initialize
from rich import print

from tqdm import tqdm
from src.generator.puzzle_generator import PuzzleGenerator
from src.utils import scoring_function

"""
testing a move generation method
"""


def move_generator(puzzle, ignore_move = None):
    # apply and score all moves from puzzle.allowed_moves
    # record the highest scoring move
    # apply this move and repeat until puzzle.validate() == True
    move_score = pd.DataFrame(columns=["move", "score"])
    moves = []
    scores =[]
    for move in puzzle.allowed_moves:
        if move == ignore_move:
            continue
        new_State = puzzle.test_moves(move)
        score = scoring_function(new_State, puzzle.solution_state)
        moves.append(move)
        scores.append(score)

    move_score["move"] = moves
    move_score["score"] = scores
    move_score = move_score.sort_values(by="score", ascending=False)
    return move_score

with initialize(version_base="1.2", config_path="run/conf"):
    cfg = compose(
        config_name="train", overrides=["config.specific_puzzle=1", "config.init_moves=false"]
    )

puzzle_generator = PuzzleGenerator(cfg)  # type: ignore
puzzles = puzzle_generator.fetch_solutions()
for puzzle in puzzles:
    print(puzzle.pid, puzzle.validate())
    print(puzzle)
    print(puzzle.previous_states)


while puzzles[0].validate() == False and len(puzzles[0].moves) < 20:
    if len(puzzles[0].moves) > 0:
        previous_move = puzzles[0].moves[-1]
        opp_previous_move = f"-{previous_move}" if len(previous_move) == 2 else previous_move[1:]
    else:
        opp_previous_move = None
    all_moves = move_generator(puzzles[0], opp_previous_move)
    move = all_moves.iloc[0]["move"]
    puzzles[0].apply_moves(move)

move_generator(puzzles[0])
