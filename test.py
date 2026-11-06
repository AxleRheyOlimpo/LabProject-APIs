import sys
import tkinter as tk

print("Running on Python:", sys.version)

root = tk.Tk()
root.title("SIA 2 Lab - System Check")
root.geometry("300x120")

label = tk.Label(root, text="Environment Ready!\nTkinter is working.", font=("Arial", 11))
label.pack(expand=True)

root.mainloop()