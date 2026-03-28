from core_funcs import Game_T14
from bot import GameBot


def print_tree(
    node,
    indent=0,
    max_print_depth=3,
    chosen_move=None,
    bot_player=0,
    _on_best_path=None,
):
    """
    Print the game tree to terminal with color coding.
    Green  ★ = Applied move branch (unbroken best-value chain from root)
    Blue   ● = Alternative best-value branch (same value, different D1 branch)
    Red    ○ = Rejected (value differs from parent, chain broken)
    """
    if node.depth > max_print_depth:
        return

    # ANSI color codes
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    is_root = node.parent is None

    # _on_best_path: is there an unbroken value chain from root to this node?
    # None = not yet computed (for root)
    if _on_best_path is None:
        _on_best_path = True  # root is always on the best path

    # Is this node selected by its parent? (value matches parent's value)
    is_selected_by_parent = False
    if is_root:
        is_selected_by_parent = True
    elif node.value == node.parent.value:
        is_selected_by_parent = True

    # Is this node on the best path? (unbroken chain from root)
    node_on_best_path = _on_best_path and is_selected_by_parent

    # Is this node on the applied move's branch?
    # At D1: move == chosen_move means applied branch
    # At D1+: parent is on applied branch AND this node is on best path
    is_on_applied = False
    if is_root:
        is_on_applied = True
    elif node.depth == 1 and node.move == chosen_move:
        is_on_applied = True
    elif node.depth == 1:
        is_on_applied = False
    elif hasattr(node, "_is_on_applied"):
        is_on_applied = node._is_on_applied

    # Color and marker selection
    if is_root:
        color = YELLOW
        marker = "★"
    elif is_on_applied and node_on_best_path:
        color = GREEN
        marker = "★"
    elif node_on_best_path:
        color = BLUE
        marker = "●"
    else:
        color = RED
        marker = "○"

    # Tree connectors
    if is_root:
        connector = ""
    elif node == node.parent.children[-1]:
        connector = "└───\t"
    else:
        connector = "├───\t"

    def build_prefix(n):
        if n.parent is None:
            return ""
        parts = []
        current = n.parent
        ancestors = []
        while current and current.parent:
            ancestors.append(current)
            current = current.parent
        ancestors.reverse()
        for a in ancestors:
            if a == a.parent.children[-1]:
                parts.append("\t")
            else:
                parts.append("│\t")
        return "".join(parts)

    prefix = build_prefix(node)

    # Turn label
    turn_label = (
        f"{BOLD}MAX{RESET}" if node.state.turn == bot_player else f"{BOLD}MIN{RESET}"
    )

    # Board
    board_str = " ".join(str(x) for x in node.state.game_board)

    # Leaf tag
    is_leaf = len(node.children) == 0
    leaf_tag = f"\t{CYAN}◄ LEAF{RESET}" if is_leaf else ""

    # Move info
    if is_root:
        move_info = f"{YELLOW}{BOLD}ROOT{RESET}"
    else:
        pair = f"{node.parent.state.game_board[node.move]}{node.parent.state.game_board[node.move+1]}"
        move_info = f"{color}m={node.move} ({pair}){RESET}"

    line = (
        f"{prefix}{connector}"
        f"{color}{marker}{RESET}\t"
        f"{color}{BOLD}D{node.depth}{RESET}\t"
        f"{move_info}\t"
        f"{DIM}│{RESET} [{board_str}]\t"
        f"{DIM}│{RESET} P1={node.state.player1_points:+d}\tP2={node.state.player2_points:+d}\t"
        f"{DIM}│{RESET} {turn_label}\t"
        f"{DIM}│{RESET} {color}{BOLD}val={node.value}{RESET}"
        f"{leaf_tag}"
    )
    print(line)

    # Print children
    for child in node.children:
        # Is child on best path?
        child_on_best = node_on_best_path and (child.value == node.value)

        # Is child on the applied branch?
        child_on_applied = False
        if child.depth == 1 and child.move == chosen_move:
            child_on_applied = True
        elif child.depth == 1:
            child_on_applied = False
        else:
            child_on_applied = is_on_applied and child_on_best

        child._is_on_applied = child_on_applied

        print_tree(
            child,
            indent=indent + 1,
            max_print_depth=max_print_depth,
            chosen_move=chosen_move,
            bot_player=bot_player,
            _on_best_path=node_on_best_path,
        )


if __name__ == "__main__":
    print("Welcome to Game T14")

    # Board size selection
    while True:
        try:
            board_size = int(input("Please enter board size (15-25): "))
            if 15 <= board_size <= 25:
                break
            else:
                print("Invalid input. Please enter a number between 15 and 25.")
        except ValueError:
            print("Invalid input. Please enter an integer between 15 and 25.")

    # Player selection
    while True:
        try:
            human_player = int(input("Play as Player 1 or Player 2? (1/2): ")) - 1
            if human_player in [0, 1]:
                break
            else:
                print("Invalid input. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

    bot_player = 1 - human_player

    # Bot settings
    while True:
        try:
            max_depth = int(input("Enter bot max depth (1-10): "))
            if 1 <= max_depth <= 10:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Tree display option
    while True:
        show_tree_input = input("Show game tree after bot moves? (y/n): ").lower()
        if show_tree_input in ["y", "n"]:
            show_tree = show_tree_input == "y"
            break
        else:
            print("Invalid input. Please enter y or n.")

    # Create game
    game_t14 = Game_T14()
    game_t14.create_new_game(board_size)

    # Create bot (algorithm=0 -> minimax)
    bot = GameBot(algorithm=0, max_depth=max_depth, bot_player=bot_player)

    human_label = f"Player {human_player + 1}"
    bot_label = f"Player {bot_player + 1} (BOT)"

    print(f"\nYou are {human_label}, Bot is {bot_label}")
    print(f"Bot algorithm: Minimax, max_depth={max_depth}\n")

    # Game loop
    while game_t14.check_is_end() == -1:
        print(f"-----------------------------------")
        print(f"Turn {game_t14.game_object.turn_count})")
        game_t14.print_status()
        game_t14.print_board()

        current_turn = game_t14.game_object.turn

        if current_turn == human_player:
            # Human makes a move
            while True:
                try:
                    max_move = len(game_t14.game_object.game_board) - 1
                    move = int(input(f"Please enter move (1-{max_move}): ")) - 1
                    if 0 <= move < len(game_t14.game_object.game_board) - 1:
                        break
                    else:
                        print("Invalid input. Please enter a valid move.")
                except ValueError:
                    print("Invalid input. Please enter an integer.")

            game_t14.turn(move)

        else:
            # Bot makes a move
            print(f"\n{bot_label} is thinking...")
            best_move, best_value, stats, root = bot.choose_move(game_t14.game_object)

            print(f"Bot chose move: {best_move + 1} (index {best_move})")
            print(
                f"  Eval: {best_value} | "
                f"Nodes: {stats['nodes_generated']} | "
                f"Leaves: {stats['nodes_evaluated']} | "
                f"Time: {stats['move_time']:.4f}s"
            )

            if show_tree:
                print(f"\n  GAME TREE (first 3 levels):")
                print(
                    f"  \033[92m★ Applied move\033[0m  \033[94m● Same value (alternative)\033[0m  \033[91m○ Rejected\033[0m"
                )
                print()
                print_tree(
                    root,
                    indent=0,
                    max_print_depth=3,
                    chosen_move=best_move,
                    bot_player=bot_player,
                )
                print()

            game_t14.turn(best_move)

    # Result
    print(f"\n{'='*40}")
    match game_t14.check_is_end():
        case 0:
            winner = "Player 1"
        case 1:
            winner = "Player 2"
        case 2:
            winner = None

    if winner is None:
        print(
            f"Draw! "
            f"P1: {game_t14.game_object.player1_points}, "
            f"P2: {game_t14.game_object.player2_points}"
        )
    else:
        result = "YOU WIN!" if winner == human_label else "BOT WINS!"
        print(
            f"{winner} wins! {result} "
            f"P1: {game_t14.game_object.player1_points}, "
            f"P2: {game_t14.game_object.player2_points}"
        )
