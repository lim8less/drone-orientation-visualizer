import serial
import json
import numpy as np
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Ensure enough arguments are passed
if len(sys.argv) < 6:
    print("Usage: python visualizer.py <COM_PORT> <BAUD_RATE> <WIDTH> <HEIGHT> <DEPTH>")
    sys.exit(1)

# Get user inputs from command-line arguments
com_port = sys.argv[1]
baud_rate = int(sys.argv[2])  # Convert baud rate to integer
width = float(sys.argv[3])
height = float(sys.argv[4])
depth = float(sys.argv[5])

# Open the serial port with the selected baud rate
try:
    ser = serial.Serial(com_port, baud_rate, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    sys.exit(1)

def get_drone_box(w, h, d):
    return np.array([
        [-w/2, -h/2, -d/2], [w/2, -h/2, -d/2], [w/2, h/2, -d/2], [-w/2, h/2, -d/2],  
        [-w/2, -h/2, d/2], [w/2, -h/2, d/2], [w/2, h/2, d/2], [-w/2, h/2, d/2]  
    ])

def rotation_matrix(roll, pitch, yaw):
    roll, pitch, yaw = np.radians([roll, pitch, yaw])
    R_x = np.array([[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]])
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)], [0, 1, 0], [-np.sin(pitch), 0, np.cos(pitch)]])
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
    return np.dot(R_z, np.dot(R_y, R_x))

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

while True:
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            data = json.loads(line)
            roll, pitch, yaw = data.get('roll', 0), data.get('pitch', 0), data.get('yaw', 0)

            box = get_drone_box(width, height, depth).T
            rotated_box = rotation_matrix(roll, pitch, yaw) @ box
            rotated_box = rotated_box.T

            faces = [
                [rotated_box[j] for j in [0, 1, 2, 3]], [rotated_box[j] for j in [4, 5, 6, 7]],
                [rotated_box[j] for j in [0, 1, 5, 4]], [rotated_box[j] for j in [2, 3, 7, 6]],
                [rotated_box[j] for j in [0, 3, 7, 4]], [rotated_box[j] for j in [1, 2, 6, 5]]
            ]

            ax.clear()
            ax.set_proj_type('persp')  

            ax.add_collection3d(Poly3DCollection(faces, facecolors=['blue', 'red', 'green', 'yellow', 'cyan', 'magenta'], 
                                                 edgecolor='black', linewidth=1.5))

            max_range = max(width, height, depth) * 1.2
            ax.set_xlim([-max_range, max_range])
            ax.set_ylim([-max_range, max_range])
            ax.set_zlim([-max_range, max_range])

            ax.set_xlabel('X (Roll)')
            ax.set_ylabel('Y (Pitch)')
            ax.set_zlabel('Z (Yaw)')
            ax.set_title(f"Roll: {roll:.1f}°, Pitch: {pitch:.1f}°, Yaw: {yaw:.1f}°")

            plt.draw()
            plt.pause(0.1)

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error processing line: {line}, Error: {e}")
