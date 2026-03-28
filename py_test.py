import pytest
from core_funcs import Game_T14


def test_create_new_game():
    game = Game_T14()
    game.create_new_game(20)

    assert len(game.game_object.game_board) == 20
    assert all(cell in [0, 1] for cell in game.game_object.game_board)
    assert game.game_object.turn == 0
    assert game.game_object.player1_points == 0
    assert game.game_object.player2_points == 0


def test_turn_player1_00():
    game = Game_T14()
    game.create_new_game(5)

    game.game_object.game_board = [0, 0, 1, 1, 0]
    game.game_object.turn = 0
    game.game_object.player1_points = 0
    game.game_object.player2_points = 0

    game.turn(0)

    assert game.game_object.game_board == [1, 1, 1, 0]
    assert game.game_object.player1_points == 1
    assert game.game_object.player2_points == 0
    assert game.game_object.turn == 1


def test_turn_player1_10():
    game = Game_T14()
    game.create_new_game(4)

    game.game_object.game_board = [1, 0, 1, 1]
    game.game_object.turn = 0
    game.game_object.player1_points = 0
    game.game_object.player2_points = 5

    game.turn(0)

    assert game.game_object.game_board == [1, 1, 1]
    assert game.game_object.player1_points == 0
    assert game.game_object.player2_points == 4
    assert game.game_object.turn == 1


def test_turn_invalid_move():
    game = Game_T14()
    game.create_new_game(4)
    game.game_object.game_board = [1, 0, 1, 1]

    with pytest.raises(ValueError):
        game.turn(3)
