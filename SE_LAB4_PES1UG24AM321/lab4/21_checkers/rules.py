SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    direction = -1 if player == "R" else 1
    return (
        board[er][ec] == "." and
        abs(er - sr) == 1 and abs(ec - sc) == 1 and
        er - sr == direction
    )


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    direction = -1 if player == "R" else 1
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    return (
        board[er][ec] == "." and
        abs(er - sr) == 2 and abs(ec - sc) == 2 and
        er - sr == 2 * direction and
        board[mr][mc] not in (".", player)
    )

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