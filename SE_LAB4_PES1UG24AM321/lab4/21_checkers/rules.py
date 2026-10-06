SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    return (
        owner(piece) == player and
        board[er][ec] == "." and
        abs(ec - sc) == 1 and
        (er - sr) in row_directions(piece)
    )


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if owner(piece) != player or board[er][ec] != ".":
        return False
    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False
    if (er - sr) // 2 not in row_directions(piece):
        return False
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    # The jumped piece must belong to the opponent (man or king).
    return owner(board[mr][mc]) not in (None, player)


def in_bounds(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def player_squares(board, player):
    """Positions of every piece (man or king) belonging to player."""
    return [
        (r, c)
        for r in range(SIZE)
        for c in range(SIZE)
        if board[r][c] in (player, player + "K")
    ]


def piece_can_move(board, player, start):
    """True if the piece on start has at least one legal move or capture."""
    sr, sc = start
    for step, is_legal in ((1, simple_move), (2, capture_move)):
        for dr in (-step, step):
            for dc in (-step, step):
                end = (sr + dr, sc + dc)
                if in_bounds(*end) and is_legal(board, player, start, end):
                    return True
    return False


def has_any_move(board, player):
    return any(piece_can_move(board, player, sq) for sq in player_squares(board, player))

def promote(board):
    """Crown men on their far row. Returns the squares that were promoted."""
    promoted = []
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted.append((0, c))
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted.append((SIZE - 1, c))
    return promoted



def captures_from(board, player, start):
    """Squares the piece on start can jump to."""
    sr, sc = start
    ends = []
    for dr in (-2, 2):
        for dc in (-2, 2):
            end = (sr + dr, sc + dc)
            if in_bounds(*end) and capture_move(board, player, start, end):
                ends.append(end)
    return ends


def has_capture(board, player):
    return any(captures_from(board, player, sq) for sq in player_squares(board, player))

def owner(piece):
    """'R' or 'B' for a piece ('R', 'RK', 'B', 'BK'), None for an empty square."""
    return None if piece == "." else piece[0]


def row_directions(piece):
    """Row steps a piece may take: kings go both ways, men only forward."""
    if piece.endswith("K"):
        return (-1, 1)
    return (-1,) if owner(piece) == "R" else (1,)