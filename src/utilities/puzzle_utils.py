from src.dtos.PuzzleDTO import PuzzleDTO


def get_number_of_moves_for_puzzle(puzzle: PuzzleDTO):
    return len(puzzle.submission_solution.split("."))
