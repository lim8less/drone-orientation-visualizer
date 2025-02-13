import tkinter as tk
from tkinter import messagebox
import subprocess

def start_visualizer():
    com_port = com_port_entry.get().strip()
    baud_rate = baud_rate_var.get()
    width = width_entry.get().strip()
    height = height_entry.get().strip()
    depth = depth_entry.get().strip()

    if not com_port or not width or not height or not depth:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        width, height, depth = float(width), float(height), float(depth)
    except ValueError:
        messagebox.showerror("Input Error", "Width, Height, and Depth must be numbers!")
        return

    try:
        subprocess.Popen(["python", "visualizer.py", com_port, str(baud_rate), str(width), str(height), str(depth)])
        root.destroy()  
    except Exception as e:
        messagebox.showerror("Error", f"Could not start visualization: {e}")

root = tk.Tk()
root.title("Drone Visualization Settings")
root.geometry("300x300")

tk.Label(root, text="Enter COM Port:").pack()
com_port_entry = tk.Entry(root)
com_port_entry.pack()

tk.Label(root, text="Baud Rate:").pack()
baud_rate_var = tk.StringVar(root)
baud_rate_var.set("115200")  
baud_rate_menu = tk.OptionMenu(root, baud_rate_var, "9600", "57600", "115200", "230400")
baud_rate_menu.pack()

tk.Label(root, text="Width:").pack()
width_entry = tk.Entry(root)
width_entry.pack()

tk.Label(root, text="Height:").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Depth:").pack()
depth_entry = tk.Entry(root)
depth_entry.pack()

start_btn = tk.Button(root, text="Start Visualization", command=start_visualizer)
start_btn.pack(pady=10)

root.mainloop()
