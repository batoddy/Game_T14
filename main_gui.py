import tkinter as tk
from tkinter import messagebox
from core_funcs import Game_T14
from bot import GameBot


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game T14 - Minimax Game")
        self.root.geometry("600x400")

        self.game = Game_T14()
        self.bot = None

        self.human_player = 0  # 0 -> Player 1, 1 -> Player 2
        self.bot_player = 1
        self.algorithm = 0  # 0 -> Minimax, 1 -> Alpha-Beta

        # ===== TOP FRAME =====
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.status_label = tk.Label(
            self.top_frame, text="Start the Game", font=("Arial", 14)
        )
        self.status_label.pack()

        self.score_label = tk.Label(self.top_frame, text="", font=("Arial", 12))
        self.score_label.pack()

        self.stats_label = tk.Label(
            self.top_frame, text="Last bot move stats: -", font=("Arial", 10)
        )
        self.stats_label.pack()

        # ===== BOARD FRAME =====
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(pady=20)

        # ===== CONTROL FRAME =====
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        tk.Label(self.control_frame, text="Board Size (15-25):").grid(row=0, column=0)
        self.size_entry = tk.Entry(self.control_frame)
        self.size_entry.insert(0, "15")
        self.size_entry.grid(row=0, column=1)

        tk.Label(self.control_frame, text="Bot Depth:").grid(row=1, column=0)
        self.depth_entry = tk.Entry(self.control_frame)
        self.depth_entry.insert(0, "3")
        self.depth_entry.grid(row=1, column=1)

        tk.Label(self.control_frame, text="Choose Player:").grid(row=2, column=0)
        self.player_var = tk.IntVar(value=0)

        tk.Radiobutton(
            self.control_frame, text="Player 1", variable=self.player_var, value=0
        ).grid(row=2, column=1, sticky="w")

        tk.Radiobutton(
            self.control_frame, text="Player 2", variable=self.player_var, value=1
        ).grid(row=2, column=2, sticky="w")

        tk.Label(self.control_frame, text="Algorithm:").grid(row=3, column=0)
        self.algorithm_var = tk.IntVar(value=0)

        tk.Radiobutton(
            self.control_frame, text="Minimax", variable=self.algorithm_var, value=0
        ).grid(row=3, column=1, sticky="w")

        tk.Radiobutton(
            self.control_frame, text="Alpha-Beta", variable=self.algorithm_var, value=1
        ).grid(row=3, column=2, sticky="w")

        self.start_btn = tk.Button(
            self.control_frame, text="Start Game", command=self.start_game
        )
        self.start_btn.grid(row=4, column=0, columnspan=3, pady=10)

    # ===== START GAME =====
    def start_game(self):
        try:
            size = int(self.size_entry.get())
            depth = int(self.depth_entry.get())
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        if not (15 <= size <= 25):
            messagebox.showerror("Error", "Board size must be between 15 and 25")
            return

        if depth < 1:
            messagebox.showerror("Error", "Depth must be at least 1")
            return

        self.human_player = self.player_var.get()
        self.algorithm = self.algorithm_var.get()
        self.bot_player = 1 if self.human_player == 0 else 0

        self.game.create_new_game(size)
        self.bot = GameBot(
            algorithm=self.algorithm, max_depth=depth, bot_player=self.bot_player
        )
        self.stats_label.config(text="Last bot move stats: -")

        self.update_ui()

        if self.game.game_object.turn == self.bot_player:
            self.root.after(500, self.bot_move)

    def update_ui(self):
        state = self.game.game_object

        # Update status
        if state.turn == self.human_player:
            player = "Your Turn"
        else:
            player = "Bot Turn"

        algo_text = "Minimax" if self.algorithm == 0 else "Alpha-Beta"
        self.status_label.config(text=f"{player} | {algo_text}")

        self.score_label.config(
            text=f"P1: {state.player1_points}   |   P2: {state.player2_points}"
        )

        # Clear board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        board = state.game_board

        # Show board numbers
        for i, val in enumerate(board):
            color = "blue" if val == 0 else "red"
            lbl = tk.Label(
                self.board_frame, text=str(val), fg=color, font=("Arial", 16), width=3
            )
            lbl.grid(row=0, column=i)

        if state.turn == self.human_player:
            for i in range(len(board) - 1):
                btn = tk.Button(
                    self.board_frame, text="↓", command=lambda i=i: self.player_move(i)
                )
                btn.grid(row=1, column=i)

        # Check end
        result = self.game.check_is_end()
        if result != -1:
            self.end_game(result)
            return

        # Bot turn
        if state.turn == self.bot_player:
            self.root.after(500, self.bot_move)

    # ===== PLAYER MOVE =====
    def player_move(self, move):
        if self.game.game_object.turn != self.human_player:
            return

        self.game.turn(move)
        self.update_ui()

    # ===== BOT MOVE =====
    def bot_move(self):
        if self.game.game_object.turn != self.bot_player:
            return

        result = self.bot.choose_move(self.game.game_object)

        if isinstance(result, tuple):
            move = result[0]
            best_value = result[1]
            stats = result[2]
        else:
            move = result
            best_value = "-"
            stats = None

        if move is None:
            return

        if stats is not None:
            self.stats_label.config(
                text=(
                    f"Last bot move stats: "
                    f"Eval={best_value} | "
                    f"Nodes={stats['nodes_generated']} | "
                    f"Leaves={stats['nodes_evaluated']} | "
                    f"Time={stats['move_time']:.4f}s"
                )
            )

        self.game.turn(move)
        self.update_ui()

    # ===== END GAME =====
    def end_game(self, result):
        if result == 2:
            msg = "Draw!"
        elif result == self.human_player:
            msg = "You Win!"
        else:
            msg = "Bot Wins!"

        messagebox.showinfo("Game Over", msg)


# ===== RUN APP =====
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
