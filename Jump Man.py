import tkinter as tk
import random

width = 600
height = 300

root = tk.Tk()
root.title("Jump Man")

canvas = tk.Canvas(root, width=width, height=height, bg="black")
canvas.pack()

ground_y = 250
canvas.create_line(0, ground_y, width, ground_y, fill="green", width=100)

player = canvas.create_rectangle(50, 210, 90, 250, fill="blue")

obstacle = canvas.create_rectangle(width, 220, width + 30, 250, fill="red")

jumping = False
velocity = 0
gravity = 1
score = 0

score_text = canvas.create_text(60, 20, text="Score: 0", font=("Arial", 14), fill="white")

def jump(event):
    global jumping, velocity
    if not jumping:
        jumping = True
        velocity = -15

root.bind("<space>", jump)

def game_loop():
    global jumping, velocity, score
    if jumping:
        canvas.move(player, 0, velocity)
        velocity += gravity
        player_pos = canvas.coords(player)
        if player_pos[3] >= ground_y:
            canvas.coords(player, 50, 210, 90, 250)
            jumping = False
            velocity = 0
    
    canvas.move(obstacle, -5, 0)
    obstacle_pos = canvas.coords(obstacle)
    
    if obstacle_pos[2] < 0:
        canvas.coords(obstacle, width, 220, width + 30, 250)
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")
    
    root.after(20, game_loop)

game_loop()
root.mainloop()