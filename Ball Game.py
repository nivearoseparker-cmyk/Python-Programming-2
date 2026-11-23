import tkinter as tk
import random

width = 500
height = 400

root = tk.Tk()
root.title("Ball Game")
canvas = tk.Canvas(root, width=width, height=height, bg="black")
canvas.pack()

score = 0
score_text = canvas.create_text(70, 20, text=f"Score: {score}", fill="white", font=("Arial", 16))

paddle_width = 100
paddle_height = 20
paddle = canvas.create_rectangle((width - paddle_width) // 2, height - paddle_height - 10,
                                  (width + paddle_width) // 2, height - 10, fill="white")
ball_size = 20
ball = canvas.create_oval(0, 0, ball_size, ball_size, fill="red")
ball_speed = 3

def move_left(event):
    canvas.move(paddle, -20, 0)

def move_right(event):
    canvas.move(paddle, 20, 0)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

def game_loop():
    global score
    canvas.move(ball, ball_speed, ball_speed)
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    if ball_pos[3] >= height:
        canvas.coords(ball, random.randint(0, width - ball_size), 0, random.randint(0, width - ball_size) + ball_size, ball_size)
        score = 0
        canvas.itemconfig(score_text, text=f"Score: {score}")

    if (ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2] and
            ball_pos[3] >= paddle_pos[1] and ball_pos[1] <= paddle_pos[3]):
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")
        
        x = random.randint(0, width - ball_size)
        canvas.coords(ball, x, 0, x + ball_size, ball_size)
        
    elif ball_pos[3] >= height:
        canvas.create_text(width // 2, height // 2, text="Game Over", fill="white", font=("Arial", 24))
        return

    root.after(30, game_loop)
game_loop()
root.mainloop()