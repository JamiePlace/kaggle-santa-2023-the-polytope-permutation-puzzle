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


def calculate_cube_face_error(solution: list, state: list, face):
    '''
             Positions                                Solution State
             +--------+                               +--------+
             | 0    1 |                               | A    A |
             |   d1   |                               |   d1   |
             | 2    3 |                               | A    A |
    +--------+--------+--------+--------+    +--------+--------+--------+--------+
    | 16  17 | 4    5 | 8   9  | 12  13 |    | E    E | B    B | C    C | D    D |
    |   r1   |   f0   |   r0   |   f1   |    |   r1   |   f0   |   r0   |   f1   |
    | 18  19 | 6    7 | 10  11 | 14  15 |    | E    E | B    B | C    C | D    D |
    +--------+--------+--------+--------+    +--------+--------+--------+--------+
             | 20  21 |                               | F    F |
             |   d0   |                               |   d0   |
             | 22  23 |                               | F    F |
             +--------+                               +--------+
    '''
    initial_list = solution
    state_list = state
    assert len(initial_list) == len(state_list)

    solution_face = get_face_face(solution, face)
    state_face = get_face_face(state, face)
    num_wrong_facelets = sum(not (s == t) for s, t in zip(solution_face, state_face))

    return num_wrong_facelets


def get_face_face(cube_as_list, face):
    sl = int(len(cube_as_list) / 6)

    if face == "d1":
        return cube_as_list[0:sl]
    elif face == "f0":
        return cube_as_list[sl:sl * 2]
    elif face == "r0":
        return cube_as_list[sl * 2:sl * 3]
    elif face == "f1":
        return cube_as_list[sl * 3:sl * 4]
    elif face == "r1":
        return cube_as_list[sl * 4:sl * 5]
    elif face == "d0":
        return cube_as_list[sl * 5:sl * 6]
