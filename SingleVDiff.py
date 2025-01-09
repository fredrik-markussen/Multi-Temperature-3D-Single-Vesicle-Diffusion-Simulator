import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FFMpegWriter
import matplotlib

matplotlib.use('Qt5Agg')

# -------------------------- Common Parameters --------------------------
num_particles = 4700        
fps = 30                    
duration = 10               
frames = fps * duration     
reflective_floor = -2000    
reflective_roof = 30000     
threshold_z = 20000         

region_x_min, region_x_max = -50000, 50000  
region_y_min, region_y_max = -50000, 50000  
region_z_min = threshold_z  
region_z_max = reflective_roof

region_area = (region_x_max - region_x_min) * (region_y_max - region_y_min)
height = region_z_max - region_z_min
volume = region_area * height

target_particles = 5
target_concentration = target_particles / volume

# -------------------------- Storage for Simulation Data --------------------------
temperatures = [310, 274, 50]
sim_data = {}  # Dictionary to store simulation results for each temperature

for temperature in temperatures:
    # ------------------ Diffusion Constant Update ---------------------
    T_ref = 310  
    D_base = 0.46e-9  
    D_m2_per_s = D_base * (temperature / T_ref)
    D_pm2_per_us = D_m2_per_s * 1e24 / 1e6  
    dt = 0.001  
    sigma = np.sqrt(2 * D_pm2_per_us * dt)

    print(f"Running simulation at {temperature} K")
    print(f"Diffusion constant: {D_pm2_per_us:.2e} pm²/µs")
    print(f"Sigma: {sigma:.2e} pm")

    # ---------------------- Initialize Positions ---------------------
    positions = np.zeros((num_particles, 3))
    radius_x = 25000  
    radius_z = 2000

    phi = np.random.uniform(0, 2 * np.pi, num_particles)
    costheta = np.random.uniform(0, 1, num_particles)
    theta = np.arccos(costheta)
    u = np.random.uniform(0, 1, num_particles)
    r = u ** (1/3)

    positions[:, 0] = (r * radius_x) * np.sin(theta) * np.cos(phi)
    positions[:, 1] = (r * radius_x) * np.sin(theta) * np.sin(phi)
    positions[:, 2] = - (r * radius_z) * np.cos(theta)

    # ------------------ Brownian Motion Simulation ------------------
    all_positions = np.zeros((frames, num_particles, 3))

    for f in range(frames):
        displacements = np.random.normal(loc=0, scale=sigma, size=(num_particles, 3))
        positions += displacements

        below_floor = positions[:, 2] < reflective_floor
        positions[below_floor, 2] = 2 * reflective_floor - positions[below_floor, 2]

        above_roof = positions[:, 2] > reflective_roof
        positions[above_roof, 2] = 2 * reflective_roof - positions[above_roof, 2]

        all_positions[f] = positions.copy()

    # ------------------ Precompute Concentration Data ------------------
    particle_counts = np.sum(all_positions[:, :, 2] > threshold_z, axis=1)
    concentration = particle_counts / volume  

    # Store simulation results in dictionary
    sim_data[temperature] = {
        'all_positions': all_positions.copy(),
        'concentration': concentration.copy()
    }

# Create common time_points array (same for all simulations since dt, fps, etc. are identical)
time_points = np.arange(frames) * dt * 1000  # in ns

# ---------------------- Set Up Multi-Axis Plot & Render ---------------------
fig = plt.figure(figsize=(12, 12))

# Create four subplots: three for 3D scatter (one per temperature), one for the concentration graph
ax3d_310 = fig.add_subplot(221, projection='3d')
ax3d_274 = fig.add_subplot(222, projection='3d')
ax3d_50 = fig.add_subplot(223, projection='3d')
axgraph = fig.add_subplot(224)

# Setup 3D axes for each temperature
for ax in [ax3d_310, ax3d_274, ax3d_50]:
    ax.set_xlim(-50000, 50000)
    ax.set_ylim(-50000, 50000)
    ax.set_zlim(-2000, reflective_roof)
    ax.set_xlabel("X (pm)")
    ax.set_ylabel("Y (pm)")
    ax.set_zlabel("Z (pm)")
ax3d_310.set_title("310K")
ax3d_274.set_title("274K")
ax3d_50.set_title("50K")

# Initialize scatter plots for each temperature at frame 0
scatter_310 = ax3d_310.scatter(sim_data[310]['all_positions'][0,:,0],
                               sim_data[310]['all_positions'][0,:,1],
                               sim_data[310]['all_positions'][0,:,2],
                               s=0.5, color='red')

scatter_274 = ax3d_274.scatter(sim_data[274]['all_positions'][0,:,0],
                               sim_data[274]['all_positions'][0,:,1],
                               sim_data[274]['all_positions'][0,:,2],
                               s=0.5, color='red')

scatter_50 = ax3d_50.scatter(sim_data[50]['all_positions'][0,:,0],
                             sim_data[50]['all_positions'][0,:,1],
                             sim_data[50]['all_positions'][0,:,2],
                             s=0.5, color='red')

time_text = ax3d_310.text2D(0.05, 0.95, "", transform=ax3d_310.transAxes)

# Setup concentration graph (axgraph)
axgraph.set_title(f"Concentration Above z = {threshold_z} pm")
axgraph.set_xlabel("Time (ns)")
axgraph.set_ylabel("Concentration (particles/pm³)")
axgraph.set_xlim(0, time_points[-1])
axgraph.set_yscale('log')

max_conc_all = max(np.max(sim_data[310]['concentration']),
                   np.max(sim_data[274]['concentration']),
                   np.max(sim_data[50]['concentration']))
desired_ymax = max(max_conc_all * 1.1, target_concentration * 10)
if max_conc_all <= 0:
    max_conc_all = target_concentration * 10
    axgraph.set_ylim(1e-18, max_conc_all)
else:
    axgraph.set_ylim(1e-18, desired_ymax)

line_310, = axgraph.plot([], [], lw=1, color='blue', label='310K')
line_274, = axgraph.plot([], [], lw=1, color='orange', label='274K')
line_50, = axgraph.plot([], [], lw=1, color='purple', label='50K')

axgraph.axhline(y=target_concentration, color='green', linestyle='--', label='5 particles threshold')

# Estimated times (in ns) placeholders
t310 = 42    
t274 = 54   
t50 = 280   

axgraph.axvline(x=t310, color='orange', linestyle=':', lw=0.5, label='Time at 310K')
axgraph.axvline(x=t274, color='purple', linestyle=':', lw=0.5, label='Time at 274K')
axgraph.axvline(x=t50, color='brown', linestyle=':', lw=0.5, label='Time at 50K')

axgraph.legend()

# --------------------- Animation Update --------------------------
def update(frame):
    current_time_ns = frame * dt * 1000
    time_text.set_text(f"Time: {current_time_ns:.2f} ns")

    scatter_310._offsets3d = (
        sim_data[310]['all_positions'][frame,:,0],
        sim_data[310]['all_positions'][frame,:,1],
        sim_data[310]['all_positions'][frame,:,2]
    )
    scatter_274._offsets3d = (
        sim_data[274]['all_positions'][frame,:,0],
        sim_data[274]['all_positions'][frame,:,1],
        sim_data[274]['all_positions'][frame,:,2]
    )
    scatter_50._offsets3d = (
        sim_data[50]['all_positions'][frame,:,0],
        sim_data[50]['all_positions'][frame,:,1],
        sim_data[50]['all_positions'][frame,:,2]
    )

    if frame > 0:
        line_310.set_data(time_points[:frame], sim_data[310]['concentration'][:frame])
        line_274.set_data(time_points[:frame], sim_data[274]['concentration'][:frame])
        line_50.set_data(time_points[:frame], sim_data[50]['concentration'][:frame])
    else:
        line_310.set_data([], [])
        line_274.set_data([], [])
        line_50.set_data([], [])

    return scatter_310, scatter_274, scatter_50, line_310, line_274, line_50, time_text

# ---------------------- Animation Rendering ---------------------
writer = FFMpegWriter(fps=fps, metadata={"title": "Multi-Temperature 3D Diffusion Simulation"}, bitrate=1800)
with writer.saving(fig, "Multi_Temperature_Diffusion.mp4", dpi=100):
    for frame in range(frames):
        update(frame)
        writer.grab_frame()

plt.close(fig)
