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

        # ===== TOP FRAME =====
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.status_label = tk.Label(self.top_frame, text="Start the Game", font=("Arial", 14))
        self.status_label.pack()

        self.score_label = tk.Label(self.top_frame, text="", font=("Arial", 12))
        self.score_label.pack()

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

        self.start_btn = tk.Button(self.control_frame, text="Start Game", command=self.start_game)
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # ===== START GAME =====
    def start_game(self):
        try:
            size = int(self.size_entry.get())
            depth = int(self.depth_entry.get())
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        self.game.create_new_game(size)
        self.bot = GameBot(algorithm=0, max_depth=depth, bot_player=1)

        self.update_ui()

    # ===== UPDATE UI =====
    def update_ui(self):
        state = self.game.game_object

        # Update status
        player = "Player 1" if state.turn == 0 else "Player 2 (Bot)"
        self.status_label.config(text=f"Turn: {player}")

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
           lbl = tk.Label(self.board_frame, text=str(val), fg=color, font=("Arial", 16), width=3)
           lbl.grid(row=0, column=i)

        # Show move buttons (pairs)
        for i in range(len(board) - 1):
            btn = tk.Button(
                self.board_frame,
                text="↓",
                command=lambda i=i: self.player_move(i)
            )
            btn.grid(row=1, column=i)

        # Check end
        result = self.game.check_is_end()
        if result != -1:
            self.end_game(result)
            return

        # Bot turn
        if state.turn == 1:
            self.root.after(500, self.bot_move)

    # ===== PLAYER MOVE =====
    def player_move(self, move):
        if self.game.game_object.turn != 0:
            return

        self.game.turn(move)
        self.update_ui()

    # ===== BOT MOVE =====
    def bot_move(self):
        result = self.bot.choose_move(self.game.game_object)
        move = result[0] if isinstance(result, tuple) else result
        self.game.turn(move)
        self.update_ui()

    # ===== END GAME =====
    def end_game(self, result):
        if result == 0:
            msg = "Player 1 Wins!"
        elif result == 1:
            msg = "Bot Wins!"
        else:
            msg = "Draw!"

        messagebox.showinfo("Game Over", msg)


# ===== RUN APP =====
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()