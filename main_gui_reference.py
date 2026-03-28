"""
main_gui_reference.py

Reference file for the GUI team.
Below you will find the complete game flow from start to finish,
showing which function to call, what it returns, and how to use it in your GUI.

This file can be run directly (for terminal testing),
but its main purpose is to show you which function to call where
in your GUI code.
"""

from core_funcs import Game_T14
from bot import GameBot
from game_state_utils import get_legal_moves


# =============================================================================
# STEP 1: CREATE THE GAME
# =============================================================================
# Get board_size (15-25) from the user.
# In the GUI this can be an input field or slider.

board_size = 20  # example value

game = Game_T14()
game.create_new_game(board_size)

# After creating the game, you can access everything through game.game_object:
#
#   game.game_object.game_board     -> [1, 0, 1, 1, 0, ...]   (list[int])
#   game.game_object.board_size     -> 20                       (int)
#   game.game_object.turn           -> 0 or 1                   (0=P1, 1=P2)
#   game.game_object.player1_points -> 0                        (int)
#   game.game_object.player2_points -> 0                        (int)
#   game.game_object.turn_count     -> 0                        (int)


# =============================================================================
# STEP 2: CREATE THE BOT
# =============================================================================
# Get the following choices from the user:
#   - Which player they want to be (0 or 1)
#   - Bot search depth (1-10, recommended 4-5 for large boards)
#   - Algorithm (0=minimax, 1=alphabeta - alphabeta not yet implemented)

human_player = 0  # human is Player 1
bot_player = 1  # bot is Player 2
max_depth = 4  # search depth
algorithm = 0  # 0 = minimax

bot = GameBot(algorithm=algorithm, max_depth=max_depth, bot_player=bot_player)


# =============================================================================
# STEP 3: GAME LOOP
# =============================================================================
# Follow the steps below for each turn.
# In the GUI this will be an event loop or button callback.

while game.check_is_end() == -1:

    # --- Display the current state in the GUI ---
    current_board = game.game_object.game_board  # [1, 0, 1, 1, ...]
    current_turn = game.game_object.turn  # 0 or 1
    p1_points = game.game_object.player1_points  # int
    p2_points = game.game_object.player2_points  # int
    turn_count = game.game_object.turn_count  # int

    # --- List of legal moves ---
    # Determines which buttons/positions are clickable in the GUI
    legal_moves = get_legal_moves(game.game_object)
    # Example: board = [1,0,1,1,0] -> legal_moves = [0, 1, 2, 3]
    # Each move selects the pair board[move] and board[move+1]
    # If move=0 is clicked, the pair board[0] and board[1] is selected

    if current_turn == human_player:
        # ----- HUMAN MOVE -----
        # Get the move from the GUI via click (0-indexed)
        # Example: if the user selects the 3rd and 4th elements -> move = 2

        move = legal_moves[0]  # PLACEHOLDER - will come from GUI user selection

        # Info you can display before applying the move:
        pair = (current_board[move], current_board[move + 1])
        print(f"Human move: index={move}, pair=({pair[0]},{pair[1]})")

        # Apply the move
        game.turn(move)

    else:
        # ----- BOT MOVE -----
        # Pass the current game_object to the bot, it calculates on its own

        best_move, best_value, stats, root = bot.choose_move(game.game_object)

        # choose_move return values:
        #   best_move   -> int, selected move index (0-indexed)
        #   best_value  -> int, minimax evaluation (positive = in bot's favor)
        #   stats       -> dict:
        #       stats["nodes_generated"]  -> int, total nodes created
        #       stats["nodes_evaluated"]  -> int, leaf nodes evaluated
        #       stats["move_time"]        -> float, computation time (seconds)
        #   root        -> TreeNode, root of the minimax tree
        #                  (use this if you want to visualize the tree)

        # Info you can display in the GUI:
        print(f"Bot move: index={best_move}")
        print(f"  Evaluation: {best_value}")
        print(f"  Nodes generated: {stats['nodes_generated']}")
        print(f"  Leaves evaluated: {stats['nodes_evaluated']}")
        print(f"  Computation time: {stats['move_time']:.4f}s")

        # Apply the move
        game.turn(best_move)

        # ----- TREE VISUALIZATION (OPTIONAL) -----
        # You can traverse the tree using the root TreeNode.
        # Below is how to access the tree structure:
        #
        # root.state          -> GameObject (root state)
        # root.value          -> int (minimax value)
        # root.children       -> list[TreeNode] (D1 nodes, one per move)
        #
        # For each child:
        #   child.move        -> int (which move was made)
        #   child.value       -> int (minimax value of this branch)
        #   child.state       -> GameObject (state after move)
        #   child.children    -> list[TreeNode] (next level)
        #   child.depth       -> int (depth in tree)
        #   child.parent      -> TreeNode (parent node)
        #
        # Example: iterate over all D1 children of root
        for child in root.children:
            is_chosen = child.move == best_move
            is_best_value = child.value == root.value
            marker = (
                "APPLIED"
                if is_chosen
                else ("ALTERNATIVE" if is_best_value else "REJECTED")
            )
            print(f"  D1 move={child.move} val={child.value} [{marker}]")


# =============================================================================
# STEP 4: GAME OVER
# =============================================================================
# check_is_end() return values:
#   -1 -> game is still in progress
#    0 -> Player 1 wins
#    1 -> Player 2 wins
#    2 -> Draw

result = game.check_is_end()

p1_final = game.game_object.player1_points
p2_final = game.game_object.player2_points

if result == 0:
    print(f"Player 1 wins! P1={p1_final}, P2={p2_final}")
elif result == 1:
    print(f"Player 2 wins! P1={p1_final}, P2={p2_final}")
else:
    print(f"Draw! P1={p1_final}, P2={p2_final}")


# =============================================================================
# NOTES FOR GUI DEVELOPMENT
# =============================================================================
#
# 1. MOVE INDEX IS 0-INDEXED
#    Board = [1, 0, 1, 1, 0]:
#    move=0 -> selects pair (1,0)
#    move=1 -> selects pair (0,1)
#    move=2 -> selects pair (1,1)
#    move=3 -> selects pair (1,0)
#    Total legal moves = len(board) - 1
#
# 2. BOARD SHRINKS AFTER EACH MOVE
#    After each move the board becomes 1 element shorter.
#    Update the board display in the GUI after every move.
#
# 3. TURN ALTERNATION
#    game.game_object.turn automatically alternates after each move (0 <-> 1).
#    Update the "current player" indicator in the GUI accordingly.
#
# 4. BOT THINKING TIME
#    On large boards (20+) with high depth (5+) the bot may slow down.
#    Consider showing a "Bot is thinking..." loading indicator in the GUI.
#    If needed, run bot.choose_move() in a separate thread.
#
# 5. TREE VISUALIZATION
#    You can recursively traverse the tree starting from the root TreeNode.
#    Each node's .value is the minimax result.
#    Children where root.value == child.value are "best move candidates".
#    The child matching best_move is the "applied move".
#
# 6. RESTARTING THE GAME
#    To start a new game, call game.create_new_game(board_size) again.
#    The same bot object can be reused, or create a new GameBot.
#
# 7. ERROR HANDLING
#    game.turn(move) raises ValueError for invalid moves.
#    In the GUI, only allow moves that are in the legal_moves list.
