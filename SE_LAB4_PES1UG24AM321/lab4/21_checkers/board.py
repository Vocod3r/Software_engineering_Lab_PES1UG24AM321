SIZE = 8

def remove_piece(board, pos):
    """Take a piece off the board and return what it was."""
    piece = board[pos[0]][pos[1]]
    board[pos[0]][pos[1]] = "."
    return piece


def jumped_square(start, end):
    """The square between start and end of a two-square diagonal jump."""
    return (start[0] + end[0]) // 2, (start[1] + end[1]) // 2

def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def move_piece(board, start, end):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."
