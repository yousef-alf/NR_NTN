## Libraries

Matplotlib: Used for 3D plotting and animation.

NumPy: Used for mathematical operations, including calculating satellite positions.

Pillow: Used to load the Earth texture image.

## Key Components

Earth Model: A 3D model of the Earth is created using a texture map. This is rendered using Matplotlib's 3D plotting capabilities.

Satellites: Three satellites are modeled with different orbital parameters (orbital_radius and orbital_period). These satellites move in their orbits over time, and their positions are updated in each frame.

Receiver: The receiver is placed at the coordinates of Riyadh (24.7136° N, 46.6753° E), and its position is displayed on the 3D plot.

NR NTN Connection: When a satellite comes within a certain distance threshold from the receiver, a simulated connection is established. The status of the connection is updated in real-time.

Animation: The simulation includes real-time animation using FuncAnimation to update the positions of the satellites and the connection status between the receiver and satellites.


## View Satellite Movement:

The satellites move along their respective orbits, and their paths are displayed as they update in each frame. The simulation stops once the maximum number of frames has been reached.

## Connection Status:

The simulation will display connection messages if a satellite comes within the connection threshold of the receiver.
