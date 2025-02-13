import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports
import subprocess

def get_available_ports():
    """Detect available COM ports and return them as a list."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def start_visualizer():
    com_port = com_port_var.get()
    baud_rate = baud_rate_var.get()
    width = width_var.get().strip()
    height = height_var.get().strip()
    depth = depth_var.get().strip()
    
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

tk.Label(root, text="Select COM Port:").pack()
com_port_var = tk.StringVar()
available_ports = get_available_ports()
com_port_dropdown = ttk.Combobox(root, textvariable=com_port_var, values=available_ports, state="readonly")
com_port_dropdown.pack()
if available_ports:
    com_port_dropdown.current(0)

tk.Label(root, text="Baud Rate:").pack()
baud_rate_var = tk.StringVar(root)
baud_rate_var.set("115200")  
baud_rate_menu = ttk.Combobox(root, textvariable=baud_rate_var, values=["9600", "57600", "115200", "230400"], state="readonly")
baud_rate_menu.pack()

tk.Label(root, text="Width:").pack()
width_var = tk.StringVar()
tk.Entry(root, textvariable=width_var).pack()

tk.Label(root, text="Height:").pack()
height_var = tk.StringVar()
tk.Entry(root, textvariable=height_var).pack()

tk.Label(root, text="Depth:").pack()
depth_var = tk.StringVar()
tk.Entry(root, textvariable=depth_var).pack()

start_btn = tk.Button(root, text="Start Visualization", command=start_visualizer)
start_btn.pack(pady=10)

root.mainloop()
