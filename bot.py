from game_state_utils import *
import time


class GameBot:
    def __init__(self, algorithm, max_depth, bot_player):
        self.algorithm = algorithm  # 0 for minmax, 1 for alphabeta
        self.max_depth = max_depth
        self.bot_player = bot_player

    def choose_move(self, state):
        legal_moves = get_legal_moves(state)

        if not legal_moves:
            return (
                None,
                None,
                {
                    "nodes_generated": 0,
                    "nodes_evaluated": 0,
                    "time_seconds": 0.0,
                },
            )

        if self.algorithm == 0:
            return self.minimax_decision(
                state=state,
                max_depth=self.max_depth,
                bot_player=self.bot_player,
            )

        elif self.algorithm == 1:
            return self.alphabeta_decision(
                state=state,
                max_depth=self.max_depth,
                bot_player=self.bot_player,
            )

        else:
            raise ValueError("Invalid algorithm selection.")

    def minimax_decision(self, state, max_depth, bot_player):
        start_time = time.time()

        stats = {"nodes_generated": 0, "nodes_evaluated": 0, "move_time": 0}

        root = TreeNode(state=state, move=None, parent=None, depth=0)
        stats["nodes_generated"] += 1

        best_move = None
        best_value = float("-inf")

        # Root'un child'larini olustur ve en iyi hamleyi bul
        legal_moves = get_legal_moves(state)
        for move in legal_moves:
            new_state = apply_move(state, move)
            child_node = root.create_child(new_state, move, root, 1)
            stats["nodes_generated"] += 1

            value = self.evaluate_node(child_node, max_depth, bot_player, stats)

            if value > best_value:
                best_value = value
                best_move = move

        root.value = best_value

        elapsed = time.time() - start_time
        stats["move_time"] = elapsed

        return best_move, best_value, stats, root

    def evaluate_node(self, node, max_depth, bot_player, stats):
        legal_moves = get_legal_moves(node.state)

        # Terminal veya depth limit -> leaf degerini dondur
        if not legal_moves or node.depth >= max_depth:
            node.value = evaluate_state(node.state, bot_player)
            stats["nodes_evaluated"] += 1
            return node.value

        # Bot'un turu -> maximize
        if node.state.turn == bot_player:
            best_value = float("-inf")
            for move in legal_moves:
                new_state = apply_move(node.state, move)
                new_node = node.create_child(new_state, move, node, node.depth + 1)
                stats["nodes_generated"] += 1

                value = self.evaluate_node(new_node, max_depth, bot_player, stats)

                if value > best_value:
                    best_value = value

        # Rakibin turu -> minimize
        else:
            best_value = float("inf")
            for move in legal_moves:
                new_state = apply_move(node.state, move)
                new_node = node.create_child(new_state, move, node, node.depth + 1)
                stats["nodes_generated"] += 1

                value = self.evaluate_node(new_node, max_depth, bot_player, stats)

                if value < best_value:
                    best_value = value

        node.value = best_value
        return best_value

    def alphabeta_decision(self, state, max_depth, bot_player):
        pass
