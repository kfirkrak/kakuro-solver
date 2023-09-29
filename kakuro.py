from board import *
from collections import deque
import time

# 0 = horizontal 1 = vertical

EXAMPLE_0 = [(3, 2, 1, 0, 1), (6, 3, 1, 0, 2),
             (4, 2, 1, 1, 3), (4, 2, 0, 1, 0),
             (6, 3, 0, 2, 0), (3, 2, 0, 3, 1)]

EXAMPLE_1 = [(16, 2, 0, 1, 0), (17, 2, 0, 2, 0),
             (35, 5, 0, 3, 0), (7, 2, 0, 4, 1),
             (16, 5, 0, 5, 2), (21, 4, 0, 6, 0),
             (6, 3, 0, 7, 0), (24, 3, 0, 1, 4),
             (29, 4, 0, 2, 3), (8, 2, 0, 4, 4),
             (5, 2, 0, 6, 5), (3, 2, 0, 7, 5),
             (23, 3, 1, 0, 1), (30, 4, 1, 0, 2),
             (15, 5, 1, 2, 3), (17, 2, 1, 1, 4),
             (27, 5, 1, 0, 5), (12, 2, 1, 0, 6),
             (16, 2, 1, 0, 7), (11, 2, 1, 5, 1),
             (10, 2, 1, 5, 2), (7, 2, 1, 4, 4),
             (12, 4, 1, 3, 6), (7, 3, 1, 4, 7)]

EXAMPLE_2 = [(20, 3, 0, 1, 1), (36, 8, 0, 2, 0),
             (13, 2, 0, 3, 0), (14, 2, 0, 4, 1),
             (13, 3, 0, 5, 1), (22, 4, 0, 6, 0),
             (39, 8, 0, 7, 0), (9, 2, 0, 8, 0),
             (3, 2, 0, 1, 6), (15, 4, 0, 3, 4),
             (23, 3, 0, 4, 4), (17, 2, 0, 5, 5),
             (8, 2, 0, 6, 6), (24, 3, 0, 8, 4),
             (15, 2, 1, 1, 1), (36, 8, 1, 0, 2),
             (11, 2, 1, 0, 3), (7, 2, 1, 0, 4),
             (22, 3, 1, 1, 5), (24, 4, 1, 1, 6),
             (37, 8, 1, 0, 7), (6, 3, 1, 0, 8),
             (23, 3, 1, 5, 1), (12, 4, 1, 3, 3),
             (20, 3, 1, 4, 4), (11, 2, 1, 6, 5),
             (16, 2, 1, 6, 6), (16, 2, 1, 5, 8)
             ]

EXAMPLE_3 = [(9, 2, 0, 1, 0), (21, 4, 0, 2, 0),
             (10, 4, 0, 3, 0), (17, 2, 0, 4, 2),
             (21, 3, 1, 0, 1), (12, 3, 1, 0, 2),
             (13, 3, 1, 1, 3), (11, 3, 1, 1, 4)]


def minimal_remaining_values(board):
    """
    :return: the location with the minimal number of remaining values to place
    """
    min_values = float('inf')
    best_tile = FLAG
    for location in board.tiles:
        cur_tile = board.get_tile(location[0], location[1])
        if cur_tile.is_visited():
            continue
        tile_num_pos = cur_tile.num_possible()
        if tile_num_pos < min_values:
            min_values = tile_num_pos
            best_tile = location
    return best_tile


def single_turn(board, board_queue, num_used_boards):
    while True:
        single_value_tile = get_single_value_tiles(board)
        if single_value_tile is not None:
            cur_tile = board.get_tile(single_value_tile[X_INDEX], single_value_tile[Y_INDEX])
            value = cur_tile.possible_values()[0]
            board.place_tile(value, single_value_tile[X_INDEX], single_value_tile[Y_INDEX])
            continue

        board.update_constraints()

        if not board.is_legal():
            return

        if board.is_complete():
            return

        best_tile = minimal_remaining_values(board)
        tile = board.get_tile(best_tile[X_INDEX], best_tile[Y_INDEX])
        if tile is None:
            board.print_board()
            return

        possible_values = tile.possible_values()

        # more than one value, so we'll push them all into the queue as new boards
        for possible in possible_values:
            num_used_boards[0] += 1
            n_board = board.one_move_board_copy(possible, best_tile[X_INDEX], best_tile[Y_INDEX])
            board_queue.append(n_board)
        return


def get_single_value_tiles(board):
    """
    Gets the first tile with a single values left to place in it
    :param board: the board we're looking at
    :return:
    """
    for tile_index, tile in board.get_tiles().items():
        if tile.num_possible() == 1 and not tile.is_visited():
            return tile_index
    return None


def solve_kakuro_new(board):
    num_used_boards = [1]
    board_queue = deque()
    board_queue.append(board)
    while len(board_queue) > 0:
        cur_b = board_queue.pop()
        single_turn(cur_b, board_queue, num_used_boards)
        if cur_b.is_complete():
            print(cur_b)
            print("Number of used boards:", num_used_boards[0])
            return


if __name__ == '__main__':
    start = time.time()
    board1 = Board(EXAMPLE_1)
    solve_kakuro_new(board1)
    end = time.time()
    print("Time to solve (seconds):", end - start)
