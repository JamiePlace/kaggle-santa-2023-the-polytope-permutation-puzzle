from src.dtos.PuzzleDTO import PuzzleDTO


def get_number_of_moves_for_puzzle(puzzle: PuzzleDTO):
    return len(puzzle.submission_solution.split("."))

def is_puzzle_solution_same(puzzle1: PuzzleDTO, puzzle2: PuzzleDTO):
    return puzzle1.submission_solution == puzzle2.submission_solution


