from core_funcs import Game_T14

if __name__ == "__main__":

    print("Welcome to Game T14")

    while True:
        try:
            board_size = int(input("Please enter board size (15-25): "))
            if 15 <= board_size <= 25:
                break
            else:
                print("Invalid input. Please enter a number between 15 and 25.")
        except ValueError:
            print("Invalid input. Please enter an integer between 15 and 25.")

    game_t14 = Game_T14()
    game_t14.create_new_game(board_size)

    while game_t14.check_is_end() == -1:
        print(f"-----------------------------------")
        print(f"Turn {game_t14.game_object.turn_count})")
        game_t14.print_status()
        game_t14.print_board()

        while True:
            try:
                max_move = len(game_t14.game_object.game_board) - 1
                move = int(input(f"Please enter move (1-{max_move}): ")) - 1

                if 0 <= move < game_t14.game_object.board_size - 1:
                    break
                else:
                    print("Invalid input. Please enter a valid move.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        game_t14.turn(move)

    match game_t14.check_is_end():
        case 0:
            print(
                f"Player 1 wins! "
                f"Player 1 points: {game_t14.game_object.player1_points}, "
                f"Player 2 points: {game_t14.game_object.player2_points}"
            )
        case 1:
            print(
                f"Player 2 wins! "
                f"Player 1 points: {game_t14.game_object.player1_points}, "
                f"Player 2 points: {game_t14.game_object.player2_points}"
            )
        case 2:
            print(
                f"Draw! "
                f"Player 1 points: {game_t14.game_object.player1_points}, "
                f"Player 2 points: {game_t14.game_object.player2_points}"
            )
