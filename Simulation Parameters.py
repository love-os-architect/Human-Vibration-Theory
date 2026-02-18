import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. Configuration (Simulation Parameters) ---
dt = 0.05
T = 200  # Total steps
K = 0.8  # Coupling Strength (E/R). Try changing this! (High=Sync, Low=Drift)
omega_A = 1.0     # Natural Frequency A
omega_B = 1.05    # Natural Frequency B (Slightly different)

# Initial State (Drama Phase: ~100 degrees difference)
theta_A = 0.0
theta_B = 1.8 
A_A = 1.0
A_B = 1.0

# --- 2. Setup Lists for History ---
history_t = []
history_dth = []
history_tau = []
history_power = []

# --- 3. Visualization Setup ---
fig = plt.figure(figsize=(12, 6))
fig.suptitle(f"Love-Dynamics Simulation (K={K}, Δω={omega_B-omega_A:.2f})", fontsize=16)

# Left Plot: Complex Plane (The Arrows)
ax_polar = fig.add_subplot(1, 2, 1, projection='polar')
ax_polar.set_ylim(0, 2.5)
ax_polar.set_title("Phase Synchronization (The Dance)")

# Arrows
arrow_A, = ax_polar.plot([], [], 'c-', linewidth=3, label='Person A') # Cyan
arrow_B, = ax_polar.plot([], [], 'm-', linewidth=3, label='Person B') # Magenta
arrow_Sum, = ax_polar.plot([], [], 'y-', linewidth=5, alpha=0.5, label='Combined (Power)') # Yellow

# Right Plot: Time Series (The Metrics)
ax_metrics = fig.add_subplot(1, 2, 2)
ax_metrics.set_xlim(0, T)
ax_metrics.set_ylim(-1.5, 4.5)
ax_metrics.set_title("Metrics over Time")
ax_metrics.grid(True, alpha=0.3)

line_tau, = ax_metrics.plot([], [], 'r--', label='Torque (Drama/Attraction)')
line_power, = ax_metrics.plot([], [], 'g-', linewidth=2, label='Power (Energy Output)')
line_dth, = ax_metrics.plot([], [], 'b:', label='Phase Diff (Distance)')

ax_metrics.legend(loc='upper right')

# --- 4. Update Function (The Physics Loop) ---
def update(frame):
    global theta_A, theta_B
    
    # (A) Calculate Dynamics
    # Kuramoto Model: dθ/dt = ω + K*sin(Δθ)
    diff = theta_B - theta_A
    d_A = omega_A + K * np.sin(diff)
    d_B = omega_B + K * np.sin(-diff)
    
    # (B) Update Angles (Time Integration)
    theta_A += d_A * dt
    theta_B += d_B * dt
    
    # (C) Calculate Metrics
    # Normalize diff to -pi ... pi
    d_theta_norm = (theta_B - theta_A + np.pi) % (2 * np.pi) - np.pi
    
    current_tau = K * np.sin(d_theta_norm)      # Torque = Drama
    
    # Complex Vectors
    z_A = A_A * np.exp(1j * theta_A)
    z_B = A_B * np.exp(1j * theta_B)
    z_Sum = z_A + z_B
    current_power = np.abs(z_Sum)**2            # Power = Love Output
    
    # (D) Append History
    history_t.append(frame)
    history_dth.append(d_theta_norm)
    history_tau.append(current_tau)
    history_power.append(current_power)
    
    # --- Visualization Updates ---
    
    # 1. Update Arrows (Polar Plot)
    arrow_A.set_data([theta_A, theta_A], [0, A_A])
    arrow_B.set_data([theta_B, theta_B], [0, A_B])
    arrow_Sum.set_data([np.angle(z_Sum), np.angle(z_Sum)], [0, np.abs(z_Sum)])
    
    # 2. Update Charts (Time Series)
    line_tau.set_data(history_t, history_tau)
    line_power.set_data(history_t, history_power)
    line_dth.set_data(history_t, history_dth)
    
    return arrow_A, arrow_B, arrow_Sum, line_tau, line_power, line_dth

# --- 5. Run Animation ---
anim = FuncAnimation(fig, update, frames=np.arange(0, T), interval=50, blit=True)
plt.show()
