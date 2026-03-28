from game_object import GameObject
import random


class Game_T14:
    def __init__(self):
        pass

    def create_new_board(self, board_size):
        game_board = [random.randint(0, 1) for _ in range(board_size)]
        return game_board

    def create_new_game(self, board_size):
        game_board = self.create_new_board(board_size=board_size)

        self.game_object = GameObject(
            game_board=game_board,
            board_size=board_size,
            turn=0,
            player1_points=0,
            player2_points=0,
        )

    def print_board(self):
        print(" ".join(str(cell) for cell in self.game_object.game_board))

    def turn(self, move):
        if move < 0 or move >= len(self.game_object.game_board) - 1:
            raise ValueError("Move is out of bounds, please select a move in bounds.")

        pair = (
            self.game_object.game_board[move],
            self.game_object.game_board[move + 1],
        )

        if self.game_object.turn == 0:  # player 1 turn
            match pair:
                case (0, 0):
                    self.game_object.player1_points += 1
                    new_value = 1
                case (0, 1):
                    self.game_object.player2_points += 1
                    new_value = 0
                case (1, 0):
                    self.game_object.player2_points -= 1
                    new_value = 1
                case (1, 1):
                    self.game_object.player1_points += 1
                    new_value = 0

            self.game_object.turn = 1

        else:  # player 2 turn
            match pair:
                case (0, 0):
                    self.game_object.player2_points += 1
                    new_value = 1
                case (0, 1):
                    self.game_object.player1_points += 1
                    new_value = 0
                case (1, 0):
                    self.game_object.player1_points -= 1
                    new_value = 1
                case (1, 1):
                    self.game_object.player2_points += 1
                    new_value = 0

            self.game_object.turn = 0

        self.game_object.turn_count += 1
        self.game_object.board_size -= 1
        self.game_object.game_board[move : move + 2] = [new_value]

    def check_is_end(
        self,
    ):  # ret -1: game continue | 0: player1 wins | 1: player2 wins | 2: draw
        string_len = len(self.game_object.game_board)

        if string_len > 1:
            return -1

        else:
            if self.game_object.player1_points > self.game_object.player2_points:
                return 0

            elif self.game_object.player1_points < self.game_object.player2_points:
                return 1

            else:
                return 2

    def print_status(self):
        current_player = "Player 1" if self.game_object.turn == 0 else "Player 2"

        print(f"Player 1 points: {self.game_object.player1_points}")
        print(f"Player 2 points: {self.game_object.player2_points}")
        print(f"Turn: {current_player}")
