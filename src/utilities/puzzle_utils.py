import numpy as np

from src.dtos.PuzzleDTO import PuzzleDTO


def get_number_of_moves_for_puzzle(puzzle: PuzzleDTO):
    return len(puzzle.submission_solution.split("."))


def is_puzzle_solution_same(puzzle1: PuzzleDTO, puzzle2: PuzzleDTO):
    return puzzle1.submission_solution == puzzle2.submission_solution


def get_random_move_from_list_of_allowed_moves(allowed_moves):
    move = list(allowed_moves)[np.random.randint(0, len(list(allowed_moves.keys())))]
    rand_num = np.random.randint(0, 2)
    if rand_num == 1:
        move = "-" + move

    return move


def get_x_lowest_error_puzzle_results(results, number):
    best_puzzles = []
    for result in results:
        if len(best_puzzles) < number:
            best_puzzles.append(result)
        else:
            for index, top_x_puzzle in enumerate(best_puzzles):
                if ((result.error_count < top_x_puzzle.error_count) &
                        (not is_puzzle_solution_same(result.puzzle, top_x_puzzle.puzzle))):
                    if (get_number_of_moves_for_puzzle(result.puzzle) <=
                            get_number_of_moves_for_puzzle(top_x_puzzle.puzzle)):
                        best_puzzles[index] = result

    lowest_error_puzzles = list(filter(lambda x: x is not None, best_puzzles))
    return lowest_error_puzzles
