%matplotlib notebook
import PIL
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
import matplotlib.animation as animation

num_satellites = 3
orbital_radius = [1.1, 1.2, 1.3]
orbital_period = [20, 25, 30]

satellite_paths = [[] for _ in range(num_satellites)]
satellite_scatter = [None] * num_satellites
satellite_colors = ['r', 'yellow', 'pink']

bm = PIL.Image.open('earthicefree.jpg')
bm = np.array(bm.resize((1024, 512))) / 256.

lons = np.linspace(-180, 180, bm.shape[1]) * np.pi / 180
lats = np.linspace(-90, 90, bm.shape[0])[::-1] * np.pi / 180

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.outer(np.cos(lons), np.cos(lats)).T
y = np.outer(np.sin(lons), np.cos(lats)).T
z = np.outer(np.ones(np.size(lons)), np.sin(lats)).T

surface = ax.plot_surface(x, y, z, rstride=4, cstride=4, facecolors=bm, shade=False, zorder=1)

ax.set_axis_off()

riyadh_lat = 24.7136 * np.pi / 180
riyadh_lon = 46.6753 * np.pi / 180

earth_radius = 1
x_riyadh = earth_radius * np.cos(riyadh_lat) * np.cos(riyadh_lon)
y_riyadh = earth_radius * np.cos(riyadh_lat) * np.sin(riyadh_lon)
z_riyadh = earth_radius * np.sin(riyadh_lat)

height_offset = 0.1
z_riyadh += height_offset

tower = ax.scatter(x_riyadh, y_riyadh, z_riyadh, color='black', s=200, label="5G Tower at Riyadh", zorder=10)

max_cycles = 1
frames_per_cycle = 150
max_frames = max_cycles * frames_per_cycle
current_frame = 0

connection_text = ax.text2D(-0.1, 0.95, 'No satellite connected', ha='left', va='top', transform=ax.transAxes, fontsize=12, color='black')
message_text = ax.text2D(-0.1, 0.90, '', ha='left', va='top', transform=ax.transAxes, fontsize=10, color='Purple')

connection_threshold = 0.2

def distance_3d(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def update(val):
    azim_angle = slider.val
    ax.view_init(elev=30, azim=45)
    update_satellites(val)
    fig.canvas.draw_idle()

def update_satellites(t):
    global satellite_paths, satellite_scatter, connection_text, message_text
    
    connected_satellite = None
    message_sequence = ''
    
    for i in range(num_satellites):
        inclination = riyadh_lat
        angle = 2 * np.pi * (t / orbital_period[i])
        
        x_sat = orbital_radius[i] * np.cos(angle) * np.cos(inclination)
        y_sat = orbital_radius[i] * np.sin(angle) * np.cos(inclination)
        z_sat = orbital_radius[i] * np.sin(inclination)
        
        satellite_paths[i].append([x_sat, y_sat, z_sat])
        
        if satellite_scatter[i] is not None:
            satellite_scatter[i].remove()
        
        satellite_scatter[i] = ax.scatter(x_sat, y_sat, z_sat, color=satellite_colors[i], s=100, zorder=2)
        
        dist = distance_3d(x_sat, y_sat, z_sat, x_riyadh, y_riyadh, z_riyadh)
        if dist < connection_threshold:
            connected_satellite = f"Connected to Satellite n{510 + i}"
            message_sequence = '''RRC Connection Setup Complete
Authentication-Request
Authentication-Response
NR-NTN-Channel-Request
NR-NTN-Channel-Allocation
Data-Request
Data-Response'''
        
        if len(satellite_paths[i]) > 1:
            path = np.array(satellite_paths[i])
            ax.plot(path[:, 0], path[:, 1], path[:, 2], color=satellite_colors[i], alpha=0.5, zorder=2)

    if connected_satellite:
        connection_text.set_text(connected_satellite)
        message_text.set_text(message_sequence)
    else:
        connection_text.set_text('No satellite connected')
        message_text.set_text('')

ax_slider = plt.axes([0.1, 0.01, 0.8, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Azimuth', 0, 360, valinit=0, valstep=1)

slider.on_changed(update)

ax.view_init(elev=30, azim=45)

ax.text2D(0.9, 0.95, 'Receiver', ha='center', va='top', transform=ax.transAxes, fontsize=12, color='black')
ax.text2D(0.9, 0.90, 'n510 Satellite', ha='center', va='top', transform=ax.transAxes, fontsize=12, color='r')
ax.text2D(0.9, 0.85, 'n511 Satellite', ha='center', va='top', transform=ax.transAxes, fontsize=12, color='yellow')
ax.text2D(0.9, 0.80, 'n512 Satellite', ha='center', va='top', transform=ax.transAxes, fontsize=12, color='pink')

def animate(i):
    global current_frame
    
    if current_frame >= max_frames:
        ani.event_source.stop()
    
    if current_frame < max_frames:
        update_satellites(i)
        current_frame += 1
    
    return []

ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 360, 1), interval=500, blit=False)

plt.show()
