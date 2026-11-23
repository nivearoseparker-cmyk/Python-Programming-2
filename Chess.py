import tkinter as tk

root = tk.Tk()
root.title("Chess")
root.geometry("640x640")

canvas = tk.Canvas(root, width=640, height=640)
canvas.pack()

for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            color = "white"
        else: color = "black"

        x1 = col * 80
        y1 = row * 80
        x2 = x1 + 80
        y2 = y1 + 80

        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="red")

board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],   
    ["", "", "", "", "", "", "", ""],   
    ["", "", "", "", "", "", "", ""],   
    ["", "", "", "", "", "", "", ""],   
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]]

pieces = {
    "K": "♔",
    "Q": "♕",
    "R": "♖",
    "B": "♗",
    "N": "♘",
    "P": "♙",
    "k": "♚",
    "q": "♛",
    "r": "♜",
    "b": "♝",
    "n": "♞",
    "p": "♟"
}

for row in range(8):
    for col in range(8):
        piece = board[row][col]
        if piece != "":
            canvas.create_text(
                col * 80 + 40, 
                row * 80 + 40, 
                text=pieces[piece], font=("Arial", 36))

def click(event):
    col = event.x // 80
    row = event.y // 80
    print(f"Clicked: {row}, {col}")

canvas.bind("<Button-1>", click)

selected_row = None
selected_col = None

def draw_board():
    canvas.delete("all")

    for row in range(8):
        for col in range(8):
            
            color = "white" if (row + col) % 2 == 0 else "black"
            
            x1 = col * 80
            y1 = row * 80
            x2 = x1 + 80
            y2 = y1 + 80

            canvas.create_rectangle(
                x1, y1, x2, y2, 
                fill=color, 
                outline="red")
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "":
                canvas.create_text(
                    col * 80 + 40 + 40 // 2,
                    row * 80 + 40 + 40 // 2, 
                    text=pieces[piece], 
                    font=("Arial", 36))
            
    if selected_row is not None:
        x1 = selected_col * 80
        y1 = selected_row * 80
        canvas.create_rectangle(
            x1, y1, x1 + 80, y1 + 80,
            outline="yellow", width=3)
        
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r = selected_row + dr
            c = selected_col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                canvas.create_oval(
                    c * 80 + 25, 
                    r * 80 + 25, 
                    c * 80 + 25, 
                    r * 80 + 25,
                    fill="green"
                    )
                
def click(event):
    global selected_row, selected_col
    col = event.x // 80
    row = event.y // 80
    
    if board[row][col] != "":
        selected_row = row
        selected_col = col
    else:
        selected_row = None
        selected_col = None
    
canvas.bind("<Button-1>", click)
    
root.mainloop()

