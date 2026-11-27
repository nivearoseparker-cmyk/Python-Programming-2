# Chess by Rose Parker (Skull Dev Ops)
# Real chess rules: check, checkmate, stalemate, castling, en passant and promotion.
# Click a piece to pick it up, then click a highlighted square to move it.
# White moves first. Press R to start a new game.
import tkinter as tk

SQ = 80                       # size of one square in pixels
LIGHT, DARK = "#f0d9b5", "#b58863"
WHITE_FILL, WHITE_EDGE = "#ffffff", "#000000"
BLACK_FILL, BLACK_EDGE = "#111111", "#ffffff"

# Lowercase = black pieces, uppercase = white pieces
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]]

# Solid symbols for both sides; color decides white or black
SYMBOL = {"k": "\u265a", "q": "\u265b", "r": "\u265c", "b": "\u265d", "n": "\u265e", "p": "\u265f"}

turn = "white"
selected = None               # (row, col) of the piece you picked up
moves = []                    # squares that piece can move to
moved = set()                 # squares whose king or rook has moved (for castling)
en_passant = None             # square a pawn can capture into en passant
last_move = None              # ((from_r, from_c), (to_r, to_c)) for highlighting


def is_white(p):
    return p != "" and p.isupper()


def owner(p):
    return "" if p == "" else ("white" if p.isupper() else "black")


def pseudo_moves(r, c, attacks_only=False):
    """Squares the piece at (r, c) could move to, before checking for check."""
    p = board[r][c]
    kind, side = p.lower(), owner(p)
    out = []

    def add(rr, cc):
        if 0 <= rr < 8 and 0 <= cc < 8 and owner(board[rr][cc]) != side:
            out.append((rr, cc))

    def slide(dirs):
        for dr, dc in dirs:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                if board[rr][cc] == "":
                    out.append((rr, cc))
                else:
                    if owner(board[rr][cc]) != side:
                        out.append((rr, cc))
                    break
                rr, cc = rr + dr, cc + dc

    if kind == "p":
        step = -1 if side == "white" else 1
        start = 6 if side == "white" else 1
        for dc in (-1, 1):
            rr, cc = r + step, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                if attacks_only or (board[rr][cc] and owner(board[rr][cc]) != side) or (rr, cc) == en_passant:
                    out.append((rr, cc))
        if not attacks_only and 0 <= r + step < 8 and board[r + step][c] == "":
            out.append((r + step, c))
            if r == start and board[r + 2 * step][c] == "":
                out.append((r + 2 * step, c))
    elif kind == "n":
        for dr, dc in ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)):
            add(r + dr, c + dc)
    elif kind == "b":
        slide(((-1, -1), (-1, 1), (1, -1), (1, 1)))
    elif kind == "r":
        slide(((-1, 0), (1, 0), (0, -1), (0, 1)))
    elif kind == "q":
        slide(((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)))
    elif kind == "k":
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    add(r + dr, c + dc)
        # Castling: king and rook unmoved, empty between, king not in or through check
        home = 7 if side == "white" else 0
        if not attacks_only and (r, c) == (home, 4) and (home, 4) not in moved and not in_check(side):
            enemy = "black" if side == "white" else "white"
            if (home, 7) not in moved and board[home][7].lower() == "r" and board[home][5] == board[home][6] == "" \
                    and not attacked(home, 5, enemy) and not attacked(home, 6, enemy):
                out.append((home, 6))
            if (home, 0) not in moved and board[home][0].lower() == "r" and board[home][1] == board[home][2] == board[home][3] == "" \
                    and not attacked(home, 3, enemy) and not attacked(home, 2, enemy):
                out.append((home, 2))
    return out


def attacked(r, c, by):
    """Is square (r, c) attacked by side `by`?"""
    for rr in range(8):
        for cc in range(8):
            if owner(board[rr][cc]) == by and (r, c) in pseudo_moves(rr, cc, attacks_only=True):
                return True
    return False


def in_check(side):
    king = "K" if side == "white" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                return attacked(r, c, "black" if side == "white" else "white")
    return False


def make_move(sr, sc, r, c):
    """Move a piece, handling castling, en passant and promotion. Returns an undo record."""
    global en_passant
    p = board[sr][sc]
    record = (sr, sc, r, c, p, board[r][c], en_passant, None, None)
    extra = None
    if p.lower() == "p" and (r, c) == en_passant and board[r][c] == "":
        extra = (sr, c, board[sr][c])           # captured pawn beside us
        board[sr][c] = ""
    if p.lower() == "k" and abs(c - sc) == 2:     # castling moves the rook too
        rook_from, rook_to = (7, 5) if c == 6 else (0, 3)
        board[r][rook_to], board[r][rook_from] = board[r][rook_from], ""
        extra = ("castle", r, rook_from, rook_to)
    board[r][c], board[sr][sc] = p, ""
    if p.lower() == "p" and r in (0, 7):
        board[r][c] = "Q" if p.isupper() else "q"
    en_passant = ((sr + r) // 2, c) if p.lower() == "p" and abs(r - sr) == 2 else None
    return record[:7] + (extra,)


def undo_move(rec):
    global en_passant
    sr, sc, r, c, p, taken, ep, extra = rec
    board[sr][sc], board[r][c] = p, taken
    if extra and extra[0] == "castle":
        _, rr, rook_from, rook_to = extra
        board[rr][rook_from], board[rr][rook_to] = board[rr][rook_to], ""
    elif extra:
        er, ec, piece = extra
        board[er][ec] = piece
    en_passant = ep


def legal_moves(r, c):
    """Moves that don't leave your own king in check."""
    side = owner(board[r][c])
    good = []
    for rr, cc in pseudo_moves(r, c):
        rec = make_move(r, c, rr, cc)
        if not in_check(side):
            good.append((rr, cc))
        undo_move(rec)
    return good


def has_any_move(side):
    return any(legal_moves(r, c) for r in range(8) for c in range(8) if owner(board[r][c]) == side)


def draw_piece(p, x, y):
    """Draw a solid piece with an outline so it shows on any square."""
    fill, edge = (WHITE_FILL, WHITE_EDGE) if is_white(p) else (BLACK_FILL, BLACK_EDGE)
    sym = SYMBOL[p.lower()]
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)):
        canvas.create_text(x + dx, y + dy, text=sym, font=("Arial", 44), fill=edge)
    canvas.create_text(x, y, text=sym, font=("Arial", 44), fill=fill)


def draw_board():
    canvas.delete("all")
    for r in range(8):
        for c in range(8):
            color = LIGHT if (r + c) % 2 == 0 else DARK
            canvas.create_rectangle(c * SQ, r * SQ, c * SQ + SQ, r * SQ + SQ, fill=color, outline="")
    if last_move:
        for r, c in last_move:
            canvas.create_rectangle(c * SQ, r * SQ, c * SQ + SQ, r * SQ + SQ, fill="#cdd26a", outline="", stipple="gray50")
    for side, king in (("white", "K"), ("black", "k")):
        if in_check(side):
            for r in range(8):
                for c in range(8):
                    if board[r][c] == king:
                        canvas.create_rectangle(c * SQ, r * SQ, c * SQ + SQ, r * SQ + SQ, outline="#e53e3e", width=5)
    if selected:
        r, c = selected
        canvas.create_rectangle(c * SQ, r * SQ, c * SQ + SQ, r * SQ + SQ, outline="#f6e05e", width=4)
    for r, c in moves:
        cx, cy = c * SQ + SQ // 2, r * SQ + SQ // 2
        if board[r][c]:
            canvas.create_oval(c * SQ + 4, r * SQ + 4, c * SQ + SQ - 4, r * SQ + SQ - 4, outline="#e53e3e", width=4)
        else:
            canvas.create_oval(cx - 12, cy - 12, cx + 12, cy + 12, fill="#38a169", outline="")
    for r in range(8):
        for c in range(8):
            if board[r][c]:
                draw_piece(board[r][c], c * SQ + SQ // 2, r * SQ + SQ // 2 + 2)


def click(event):
    global selected, moves, turn, last_move
    if turn == "over":
        return
    c, r = event.x // SQ, event.y // SQ
    if not (0 <= r < 8 and 0 <= c < 8):
        return
    if selected and (r, c) in moves:
        sr, sc = selected
        make_move(sr, sc, r, c)
        moved.update({(sr, sc), (r, c)})
        last_move = ((sr, sc), (r, c))
        selected, moves = None, []
        mover, turn = turn, ("black" if turn == "white" else "white")
        if not has_any_move(turn):
            if in_check(turn):
                status.config(text=f"Checkmate! {mover.title()} wins. Press R to play again.")
            else:
                status.config(text="Stalemate, it's a draw. Press R to play again.")
            turn = "over"
        elif in_check(turn):
            status.config(text=f"{turn.title()} is in check!")
        else:
            status.config(text=f"{turn.title()} to move")
    elif owner(board[r][c]) == turn:
        selected, moves = (r, c), legal_moves(r, c)
    else:
        selected, moves = None, []
    draw_board()


def reset(event=None):
    global board, turn, selected, moves, en_passant, last_move
    board[:] = [list(row) for row in START]
    turn, selected, moves, en_passant, last_move = "white", None, [], None, None
    moved.clear()
    status.config(text="White to move")
    draw_board()


START = [list(row) for row in board]

root = tk.Tk()
root.title("Chess")
canvas = tk.Canvas(root, width=8 * SQ, height=8 * SQ, highlightthickness=0)
canvas.pack()
status = tk.Label(root, text="White to move", font=("Arial", 16))
status.pack(pady=6)
canvas.bind("<Button-1>", click)
root.bind("r", reset)
root.bind("R", reset)

draw_board()
root.mainloop()
