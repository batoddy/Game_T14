import tkinter as tk
from tkinter import messagebox
from core_funcs import Game_T14
from bot import GameBot
from game_state_utils import get_legal_moves


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game T14")
        self.root.geometry("1200x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f8")

        self.game = None
        self.bot = None

        self.human_player = 0
        self.bot_player = 1
        self.max_depth = 3
        self.algorithm = 0
        self.last_bot_info = ""

        self.build_start_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_start_screen(self):
        self.clear_window()
        self.root.configure(bg="#f4f6f8")

        container = tk.Frame(self.root, bg="#f4f6f8")
        container.pack(expand=True)

        card = tk.Frame(container, bg="white", bd=2, relief="groove", padx=40, pady=35)
        card.pack()

        title = tk.Label(
            card,
            text="Game T14",
            font=("Arial", 26, "bold"),
            bg="white",
            fg="#1f2937"
        )
        title.pack(pady=(0, 20))

        subtitle = tk.Label(
            card,
            text="Human vs Bot",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#374151"
        )
        subtitle.pack(pady=(0, 8))

        algo_label = tk.Label(
            card,
            text="Algorithm: Minimax",
            font=("Arial", 12),
            bg="white",
            fg="#6b7280"
        )
        algo_label.pack(pady=(0, 20))

        info = tk.Label(
            card,
            text="Enter board size between 15 and 25",
            font=("Arial", 14),
            bg="white",
            fg="#111827"
        )
        info.pack(pady=(0, 10))

        self.board_size_entry = tk.Entry(
            card,
            font=("Arial", 15),
            justify="center",
            width=10
        )
        self.board_size_entry.pack(pady=(0, 20))
        self.board_size_entry.insert(0, "15")

        start_button = tk.Button(
            card,
            text="Start Game",
            font=("Arial", 14, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=14,
            pady=8,
            command=self.start_game
        )
        start_button.pack()

    def start_game(self):
        try:
            board_size = int(self.board_size_entry.get())

            if not 15 <= board_size <= 25:
                messagebox.showerror("Invalid Input", "Board size must be between 15 and 25.")
                return

            self.game = Game_T14()
            self.game.create_new_game(board_size)

            self.bot = GameBot(
                algorithm=self.algorithm,
                max_depth=self.max_depth,
                bot_player=self.bot_player
            )

            self.last_bot_info = ""
            self.build_game_screen()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def build_game_screen(self):
        self.clear_window()
        self.root.configure(bg="#f4f6f8")

        main = tk.Frame(self.root, bg="#f4f6f8", padx=20, pady=20)
        main.pack(fill="both", expand=True)

        header = tk.Frame(main, bg="white", bd=2, relief="groove", padx=20, pady=15)
        header.pack(fill="x", pady=(0, 15))

        self.turn_label = tk.Label(
            header,
            text="",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#111827"
        )
        self.turn_label.pack(pady=(0, 10))

        self.score_label = tk.Label(
            header,
            text="",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#374151"
        )
        self.score_label.pack()

        board_card = tk.Frame(main, bg="white", bd=2, relief="groove", padx=20, pady=20)
        board_card.pack(fill="x", pady=(0, 15))

        board_title = tk.Label(
            board_card,
            text="Current Board",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#1f2937"
        )
        board_title.pack(pady=(0, 12))

        self.board_label = tk.Label(
    board_card,
    text="",
    font=("Courier New", 20, "bold"),
    bg="white",
    fg="#111827",
    wraplength=1100,
    justify="center"
)
        self.board_label.pack()

        moves_card = tk.Frame(main, bg="white", bd=2, relief="groove", padx=20, pady=20)
        moves_card.pack(fill="both", expand=True, pady=(0, 15))

        moves_title = tk.Label(
            moves_card,
            text="Available Moves",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#1f2937"
        )
        moves_title.pack(pady=(0, 12))

        self.moves_frame = tk.Frame(moves_card, bg="white")
        self.moves_frame.pack()

        self.status_label = tk.Label(
            moves_card,
            text="",
            font=("Arial", 12),
            bg="white",
            fg="#374151",
            wraplength=900,
            justify="center"
        )
        self.status_label.pack(pady=(18, 10))

        bottom = tk.Frame(main, bg="#f4f6f8")
        bottom.pack(fill="x")

        self.restart_button = tk.Button(
            bottom,
            text="Restart",
            font=("Arial", 13, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            width=12,
            pady=8,
            command=self.build_start_screen
        )
        self.restart_button.pack()

        self.refresh_game_screen()

    def refresh_game_screen(self):
        state = self.game.game_object

        current_player_text = "Player 1 (Human)" if state.turn == 0 else "Player 2 (Bot)"
        self.turn_label.config(text=f"Turn: {current_player_text}")

        self.score_label.config(
            text=f"Player 1 Score: {state.player1_points}    |    Player 2 Score: {state.player2_points}"
        )

        self.board_label.config(text="  ".join(str(x) for x in state.game_board))

        for widget in self.moves_frame.winfo_children():
            widget.destroy()

        result = self.game.check_is_end()
        if result != -1:
            self.show_game_over(result)
            return

        legal_moves = get_legal_moves(state)

        if state.turn == self.human_player:
            text = "Choose a pair to play."
            if self.last_bot_info:
                text += f"   |   {self.last_bot_info}"
            self.status_label.config(text=text)

            for i, move in enumerate(legal_moves):
                pair_text = f"{move}: ({state.game_board[move]}, {state.game_board[move + 1]})"

                btn = tk.Button(
                    self.moves_frame,
                    text=pair_text,
                    font=("Arial", 12, "bold"),
                    width=14,
                    height=2,
                    bg="#e5e7eb",
                    fg="#111827",
                    activebackground="#d1d5db",
                    command=lambda m=move: self.handle_human_move(m)
                )
                row = i // 4
                col = i % 4
                btn.grid(row=row, column=col, padx=8, pady=8)
        else:
            self.status_label.config(text="Bot is thinking...")
            self.root.after(500, self.handle_bot_move)

    def handle_human_move(self, move):
        try:
            self.game.turn(move)
            self.refresh_game_screen()
        except ValueError as e:
            messagebox.showerror("Move Error", str(e))

    def handle_bot_move(self):
        state = self.game.game_object
        best_move, best_value, stats, root = self.bot.choose_move(state)

        self.game.turn(best_move)
        self.last_bot_info = (
            f"Bot chose move {best_move} | Eval: {best_value} | Nodes: {stats['nodes_generated']}"
        )
        self.refresh_game_screen()

    def show_game_over(self, result):
        state = self.game.game_object

        if result == 0:
            result_text = "Player 1 (Human) wins!"
        elif result == 1:
            result_text = "Player 2 (Bot) wins!"
        else:
            result_text = "Draw!"

        self.turn_label.config(text="Game Over")
        self.status_label.config(
            text=f"{result_text} Final Score -> P1: {state.player1_points}, P2: {state.player2_points}"
        )

        for widget in self.moves_frame.winfo_children():
            widget.destroy()

        end_label = tk.Label(
            self.moves_frame,
            text=result_text,
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#059669"
        )
        end_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()