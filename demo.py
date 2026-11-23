import tkinter as tk

def start():
    print("Start")

def exit():
    print("Exit")
    
def hop():
    print("Jump")

def slide():
    print("Slide")

def hit():
    print("-10")

root = tk.Tk()

root.title("Jumpman")

root.geometry("400x300")

label = tk.Label(root, text="Welcome")
label.pack()

start_button = tk.Button(root, text="Start", bg="blue", command=start)
start_button.pack()

exit_button = tk.Button(root, text="Exit", bg="red", command=exit)
exit_button.pack()

jump_button = tk.Button(root, text="Jump", bg="green", command=hop)
jump_button.pack()

slide_button = tk.Button(root, text="Slide", bg="orange", command=slide)
slide_button.pack()

hit_button = tk.Button(root, text="Punch", bg="red", command=hit)
hit_button.pack()

root.mainloop()
