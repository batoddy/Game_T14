from game_object import GameObject
from tree_node import TreeNode


def get_legal_moves(state):
    return list(range(len(state.game_board) - 1))


def apply_move(state, move):
    if move < 0 or move >= len(state.game_board) - 1:
        raise ValueError("Move is out of bounds.")

    new_state = state.copy()

    pair = (
        new_state.game_board[move],
        new_state.game_board[move + 1],
    )

    if new_state.turn == 0:  # player 1 turn
        match pair:
            case (0, 0):
                new_state.player1_points += 1
                new_value = 1
            case (0, 1):
                new_state.player2_points += 1
                new_value = 0
            case (1, 0):
                new_state.player2_points -= 1
                new_value = 1
            case (1, 1):
                new_state.player1_points += 1
                new_value = 0

        new_state.turn = 1

    else:  # player 2 turn
        match pair:
            case (0, 0):
                new_state.player2_points += 1
                new_value = 1
            case (0, 1):
                new_state.player1_points += 1
                new_value = 0
            case (1, 0):
                new_state.player1_points -= 1
                new_value = 1
            case (1, 1):
                new_state.player2_points += 1
                new_value = 0

        new_state.turn = 0

    new_state.turn_count += 1
    new_state.game_board[move : move + 2] = [new_value]

    return new_state


def evaluate_state(state, bot_player):
    if bot_player == 0:
        return state.player1_points - state.player2_points
    else:
        return state.player2_points - state.player1_points
