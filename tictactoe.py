# Enoch Muwanguzi
# 22 Dec 2022
# Tic Tac Toe with Tkinter


import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple


"""Define a Player class. The .label attribute will store the player signs, X and O
   The .color attribute will hold a string with a tkinter color"""
class Player(NamedTuple):
    label: str
    color: str


"""Define a Move class. The .row and .col attributes hold the coordinates that identify
   the moves target cell. The .label attribute will hold the sign that identifies the player"""
class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS=(
    Player(label="X", color="blue"),
    Player(label="O", color="red"),
)

"""Create a class to represent the game logic
This class will take two parametres players and board_size. The board_size argument will hold a
number representing the size of the game board"""

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        #the .players attribute calls cycle() from the itertools module
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves =[]
        #Boolean to determine if the game has a winner or not
        self._has_winner = False
        #List of player's moves in a given game
        self._winning_combos = []
        self._setup_board()
    """In _setup_board(), you use a list comprehension to provide an initial list of values
        for ._current_moves."""
    def _setup_board(self):
        self._current_moves=[
            [Move(row,col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        #Call ._get_winning_combos() and assign its return value to ._winning_combos
        self.winning_combos = self._get_winning_combos()

    """Figure out the winning combinations. This will be done by using 4 list comprehensions """
    def _get_winning_combos(self):
        rows =[
            [(move.row,move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]


    """Validating players moves. A valid move must fulfil two conditions
    1. The game does not have a winner
    2. The selected move has not already been played"""

    #_is_valid_move() method takes the move object as an argument
    def _is_valid_move(self,move):
        """Return True if the move is valid or false otherwise"""
        row,col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self,move):
        """Process the current move and check if it's a win"""
        row,col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            """Run a generator expression that retrieves all the labels from the moves in 
            the current winning combination """
            results = set(
                self._current_moves[n][m].label
                for n,m in combo
            )
            is_win = (len(results)==1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner

    """Check for tied games. Two conditions must be fulfilled 
    1. All possible moves have been played 
    2. The game has no winner"""

    def is_tied(self):
        """Return True if the game is tied and False otherwise"""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        """Return a toggled player"""
        self.current_player = next(self._players)

    def reset_game(self):
        """Reset the game state to play again"""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []




# Create a class to represent the game board
class TicTacToeBoard(tk.Tk):
    def __init__(self,game):
        # The TicTacToeBoard should inherit from Tk to make it a fully fledged GUI window
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        """This empty dictionary will map the buttons or cells on the game board corresponding
            coorindates i.e. rows and columns 
        """
        self._cells = {}
        self._game = game
        self._create_menu()
        # These two lines put together the game board by adding the display and grids of cells
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    # Create a display where you can provide informaton about the game's state result
    # For this display, the Frame widget will be used as the display panel and a Label widget
    def _create_board_display(self):
        # Create a Frame object to hold the game display
        display_frame = tk.Frame(master=self)
        # Use the .pack() geometry manager to place the frame object on the main window's top border
        """Set the fill argument to tk.X to ensure that when the user resizes the window, the frame object
        fits the entire width"""
        display_frame.pack(fill=tk.X)
        # Create a Label object
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        # Pack the display label inside the frame using the .pack() geometry manager
        self.display.pack()

        # Create grid of cells using button objects
    def _create_board_grid(self):
        # Create a frame object to hold the game's grid of cells
        grid_frame = tk.Frame(master=self)
        # Using the .pack() geometry manager to place the frame object on the main window
        grid_frame.pack()
        # Start a loop that iterates from 0 to 2. These numbers represent the row coordinates of each cell on the grid
        for row in range(self._game.board_size):
            # Configure the width and minimum size of every cell on the grid
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            # loop over the column coordinates
            for col in range(self._game.board_size):
                # Create a button object for every cell on the grid
                button = tk.Button(
                master=grid_frame,
                text="",
                font=font.Font(size=36, weight="bold"),
                fg="black",
                width=3,
                height=2,
                highlightbackground="lightblue",
                    )
                """Add a every button to the .cells dictionary. The button will work as keys, and their coordinates
                expressed as (row,col) will work as values"""
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                # Add every button to the main window using the .grid() geometry manager
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self,event):
        """Handle a player's move"""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game._is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)



    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color
    #Highlight the winning cells once a given player makes a winning move
    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")


def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()
