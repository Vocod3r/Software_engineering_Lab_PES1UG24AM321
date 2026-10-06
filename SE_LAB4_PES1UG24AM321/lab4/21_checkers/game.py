from board import initial_board, move_piece, remove_piece, jumped_square, SIZE
from rules import (
    simple_move, capture_move, promote,
    captures_from, has_capture, has_any_move, player_squares,
)

class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.chain= None

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))
            
    def read_move(self):
        try:
            raw = input(f"{self.player}> ").strip().lower().split()
        except EOFError:
            return "quit"
        if raw in (["q"], ["quit"]):
            return "quit"
        if len(raw) != 4:
            print("Enter four coordinates.")
            return None
        try:
            sr, sc, er, ec = map(int, raw)
        except ValueError:
            print("Coordinates must be numbers.")
            return None
        if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
            print("Outside board.")
            return None
        if self.board[sr][sc] not in (self.player, self.player + "K"):
            print("That is not your piece.")
            return None
        return (sr, sc), (er, ec)

    def run(self):
        print("Checkers — move: sr sc er ec (q to quit)")
        while True:
            self.print_board()
 
            if self.chain is None:
                message = self.game_over_message()
                if message:
                    print(message)
                    return
 
            move = self.read_move()
            if move == "quit":
                print("Game ended.")
                return
            if move is None:
                continue
            start, end = move
 
            if self.chain is not None and start != self.chain:
                print(f"You must keep jumping with the piece at {self.chain[0]} {self.chain[1]}.")
                continue
 
            if capture_move(self.board, self.player, start, end):
                middle = jumped_square(start, end)
                move_piece(self.board, start, end)
                taken = remove_piece(self.board, middle)
                result = (f"{self.player} captured {taken} at {middle[0]} {middle[1]} "
                          f"({start[0]} {start[1]} -> {end[0]} {end[1]}).")
                if end in promote(self.board):
                    result += " Promoted to king!"
                elif captures_from(self.board, self.player, end):
                    # Multi-capture: same player, same piece, goes again.
                    self.chain = end
                    print(result + " Another jump is available: go again.")
                    continue
            elif simple_move(self.board, self.player, start, end):
                if has_capture(self.board, self.player):
                    print("A capture is available, so you must capture.")
                    continue
                move_piece(self.board, start, end)
                result = f"{self.player} moved {start[0]} {start[1]} -> {end[0]} {end[1]}."
                if end in promote(self.board):
                    result += " Promoted to king!"
            else:
                print("Invalid move.")
                continue
 
            print(result)
            self.chain = None
            self.player = self.opponent()
            
            
    def opponent(self):
        return "B" if self.player == "R" else "R"

    def game_over_message(self):
        """Why the current player has lost, or None if the game continues."""
        if not player_squares(self.board, self.player):
            return f"{self.player} has no pieces left. {self.opponent()} wins!"
        if not has_any_move(self.board, self.player):
            return f"{self.player} has no legal moves. {self.opponent()} wins!"
        return None