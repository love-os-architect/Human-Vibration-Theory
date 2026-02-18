import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
# Scenario 1: High Resistance (Ego blocks love) -> R = 5.0
# Scenario 2: Twin Ray State (Flow state)       -> R = 0.5
R = 0.5           # Resistance (Try changing this!)
E = 1.0           # Energy Input
alpha = 2.0       # Coefficient
K = alpha * (E/R) # Coupling Strength (Derived from Love-Physics)

# Soul Frequencies (Omega)
omega_A = 1.0     # Person A's rhythm
omega_B = 1.1     # Person B's rhythm (Slightly different)
dt = 0.05
steps = 200

# Initialization
t = np.linspace(0, steps*dt, steps)
phi_A = np.zeros(steps)
phi_B = np.zeros(steps)
phi_A[0] = 0.0             # Start at different phases
phi_B[0] = np.pi           # Completely opposite start (180 degrees)

# --- Dynamics (Kuramoto Model) ---
for i in range(steps - 1):
    d_phi = phi_B[i] - phi_A[i]
    
    # Update phases based on equations
    phi_A[i+1] = phi_A[i] + (omega_A + K * np.sin(d_phi)) * dt
    phi_B[i+1] = phi_B[i] + (omega_B + K * np.sin(-d_phi)) * dt

# Compute Real Part (Projected on "Others-Axis") for visualization
wave_A = np.cos(phi_A)
wave_B = np.cos(phi_B)
resonance = np.cos(phi_A - phi_B) # 1.0 = Perfect Sync, -1.0 = Conflict

# --- Plotting ---
plt.figure(figsize=(10, 6))

# Subplot 1: The Waves
plt.subplot(2, 1, 1)
plt.plot(t, wave_A, label='Person A (Wave)', color='cyan', alpha=0.8)
plt.plot(t, wave_B, label='Person B (Wave)', color='magenta', alpha=0.8)
plt.title(f'Love Synchronization Simulation (Resistance R={R}, Coupling K={K:.2f})')
plt.ylabel('State on Real Axis')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)

# Subplot 2: Resonance Level
plt.subplot(2, 1, 2)
plt.plot(t, resonance, color='lime', linewidth=2)
plt.axhline(y=1.0, color='white', linestyle='--', alpha=0.5)
plt.title('Resonance Level (Cos(Δφ))')
plt.ylabel('Sync Score (1=Twin Ray)')
plt.xlabel('Time')
plt.ylim(-1.1, 1.1)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.style.use('dark_background')
plt.show()
