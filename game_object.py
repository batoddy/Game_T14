class GameObject:
    def __init__(
        self,
        game_board,
        board_size,
        turn,
        player1_points,
        player2_points,
        turn_count=0,
    ):
        self.game_board = game_board
        self.board_size = board_size
        self.turn = turn
        self.player1_points = player1_points
        self.player2_points = player2_points
        self.turn_count = turn_count

    def copy(self):
        return GameObject(
            game_board=self.game_board[:],
            board_size=self.board_size,
            turn=self.turn,
            player1_points=self.player1_points,
            player2_points=self.player2_points,
            turn_count=self.turn_count,
        )
