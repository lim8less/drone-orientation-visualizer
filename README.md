# Drone Orientation Visualizer

This application visualizes real-time drone movement using roll, pitch, and yaw angles.

## Features
- Accepts serial data from a NodeMCU.
- Visualizes drone movement in 3D.
- Allows selection of COM port, baud rate, and drone dimensions.

## Setup
1. Install dependencies:  
   ```
   pip install pyserial numpy matplotlib
   ```
2. Run the application:  
   ```
   python app.py
   ```

## Required Data Format
The **NodeMCU** should send JSON data as follows:
```json
{"roll": 10.5, "pitch": -5.2, "yaw": 30.0}
```

## Supported Baud Rates
- 9600  
- 57600  
- 115200 (default)  
- 230400  

