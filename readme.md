# Game T14 - Minimax Game Bot

A two-player game played on a binary string (0s and 1s). Players take turns selecting adjacent pairs to earn points. The bot uses the minimax algorithm to choose optimal moves.

## Game Rules

A random binary string of length 15-25 is generated at the start. Players take turns selecting a pair of two adjacent numbers. The pair is replaced by a single number (the string shrinks by 1 each turn). The game ends when only one number remains. The player with more points wins.

**Pair rules (from the active player's perspective):**

| Pair | Result | Point effect     |
| ---- | ------ | ---------------- |
| 0, 0 | 1      | +1 to player     |
| 0, 1 | 0      | +1 to opponent   |
| 1, 0 | 1      | -1 from opponent |
| 1, 1 | 0      | +1 to player     |

## File Structure

```
game_object.py        Game state data class (GameObject)
tree_node.py          Tree node data structure (TreeNode)
game_state_utils.py   Move application, legal move listing, evaluation functions
core_funcs.py         Game engine - create game, apply moves, check end (Game_T14)
bot.py                Minimax bot (GameBot) - recursive tree search via evaluate_node
main.py               Terminal interface - human vs bot game + tree visualization
main_gui_reference.py Reference file for GUI integration (documented below)
py_test.py            Pytest tests
```

## Quick Start (Terminal)

```bash
python main.py
```

You will be prompted for board size, player choice, bot depth, and tree display preference.

## Classes and Functions

### GameObject (`game_object.py`)

Holds the current state of the game.

**Fields:**

- `game_board` — current number sequence (list[int])
- `board_size` — length of the sequence
- `turn` — whose turn it is (0 = Player 1, 1 = Player 2)
- `player1_points`, `player2_points` — player scores
- `turn_count` — total number of moves made

**Methods:**

- `copy()` — returns a deep copy (used by minimax to copy state during tree search)

### TreeNode (`tree_node.py`)

Node in the minimax game tree.

**Fields:**

- `state` — the GameObject at this node
- `move` — the move index that led to this node
- `parent` — reference to the parent node
- `depth` — depth in the tree (root = 0)
- `children` — list of child nodes
- `value` — minimax evaluation result

**Methods:**

- `create_child(state, move, parent, depth)` — creates a new child node and appends it to the children list

### Game_T14 (`core_funcs.py`)

Main game engine. Creates games, applies moves, checks for end conditions.

**Methods:**

- `create_new_game(board_size)` — starts a new game, creates self.game_object
- `turn(move)` — applies a move (0-indexed), updates game_object
- `check_is_end()` — returns -1: continue, 0: P1 wins, 1: P2 wins, 2: draw
- `print_board()` — prints the board to terminal
- `print_status()` — prints scores and current player

### GameBot (`bot.py`)

Bot that selects optimal moves using the minimax algorithm.

**Constructor:**

- `algorithm` — 0: minimax, 1: alpha-beta (not yet implemented)
- `max_depth` — search depth limit
- `bot_player` — which player the bot controls (0 or 1)

**Methods:**

- `choose_move(state)` — returns the best move: `(best_move, best_value, stats, root)`
  - `best_move` — selected move index (0-indexed)
  - `best_value` — minimax evaluation
  - `stats` — dict: nodes_generated, nodes_evaluated, move_time
  - `root` — TreeNode root of the game tree (for visualization)
- `evaluate_node(node, max_depth, bot_player, stats)` — recursive minimax, checks state.turn to decide max/min

### Utility Functions (`game_state_utils.py`)

- `get_legal_moves(state)` — returns list of legal move indices [0, 1, ..., len(board)-2]
- `apply_move(state, move)` — copies state, applies move, returns new state
- `evaluate_state(state, bot_player)` — heuristic value: bot_score - opponent_score
- `expand_node(node)` — creates all child nodes (optional utility)

## GUI Integration

The `main_gui_reference.py` file contains the complete game flow with detailed comments explaining every function call, return value, and how to use them in a GUI. Use it as your reference when building the GUI.

##  GUI Interface

A GUI was implemented using Tkinter.

Features:
- Interactive board display
- Clickable moves
- Real-time score updates
- Bot integration using Minimax
- Game over popup

Run the GUI:

```bash
python main_gui.py

## TODO

- [ ] Alpha-beta pruning implementation (`bot.py` → `alphabeta_decision`)
- [ ] GUI interface
- [ ] Report
