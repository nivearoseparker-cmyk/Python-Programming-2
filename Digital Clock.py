import tkinter as tk

from time import strftime

root = tk.Tk()
root.title("Digital Clock")
root.geometry("400x200")

def update_time():
    current_time = strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)

clock_label = tk.Label(root, font=("Arial", 48), bg="black", fg="white")
clock_label.pack(expand=True)
update_time()
root.mainloop()