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
    Agaci terminale renkli yazdir.
    Yesil  ★ = Uygulanan hamlenin dali (root'tan leaf'e kesintisiz best-value zinciri)
    Mavi   ● = Alternatif best-value dali (root'tan leaf'e kesintisiz ama farkli D1 dalinda)
    Kirmizi○ = Secilmeyen (parent value'dan farkli, zincir kirilmis)
    """
    if node.depth > max_print_depth:
        return

    # ANSI renk kodlari
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    is_root = node.parent is None

    # _on_best_path: root'tan bu node'a kadar kesintisiz value zinciri var mi?
    # None = henuz hesaplanmadi (root icin)
    if _on_best_path is None:
        _on_best_path = True  # root her zaman best path uzerinde

    # Bu node parent'in secimi mi? (value eslesiyor mu)
    is_selected_by_parent = False
    if is_root:
        is_selected_by_parent = True
    elif node.value == node.parent.value:
        is_selected_by_parent = True

    # Bu node best path uzerinde mi? (root'tan buraya kadar hep zincir)
    node_on_best_path = _on_best_path and is_selected_by_parent

    # Bu node uygulanan move'un dalinda mi?
    # D1 de: move == chosen_move ise uygulanan dal
    # D1+ de: parent uygulanan daldaysa ve bu node da best path'te ise
    is_on_applied = False
    if is_root:
        is_on_applied = True
    elif node.depth == 1 and node.move == chosen_move:
        is_on_applied = True
    elif node.depth == 1:
        is_on_applied = False
    elif hasattr(node, "_is_on_applied"):
        is_on_applied = node._is_on_applied

    # Renk ve marker
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

    # Agac cizgileri
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

    # Turn etiketi
    turn_label = (
        f"{BOLD}MAX{RESET}" if node.state.turn == bot_player else f"{BOLD}MIN{RESET}"
    )

    # Board
    board_str = " ".join(str(x) for x in node.state.game_board)

    # Leaf
    is_leaf = len(node.children) == 0
    leaf_tag = f"\t{CYAN}◄ LEAF{RESET}" if is_leaf else ""

    # Move bilgisi
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

    # Child'lari yazdir
    for child in node.children:
        # Child best path uzerinde mi?
        child_on_best = node_on_best_path and (child.value == node.value)

        # Child uygulanan dal uzerinde mi?
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
