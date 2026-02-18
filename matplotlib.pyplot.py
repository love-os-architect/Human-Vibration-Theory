import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
steps = 300
dt = 0.1
t = np.linspace(0, steps*dt, steps)

# Natural Frequencies (omega)
# A and B are close (compatible), C is different
wA = 1.0
wB = 1.02
wC = 1.3

# Initial Phases
thetaA = np.zeros(steps)
thetaB = np.zeros(steps) + 0.1 # Start near A
thetaC = np.zeros(steps) + 1.5 # Start near 90 deg difference to A

# Coupling Strengths (K)
K_AB = 2.0  # Strong bond between A and B
K_AC = 0.0  # Initially no bond between A and C

# Metric tracking
resonance_AB = np.zeros(steps)

# --- Simulation Loop ---
for i in range(steps - 1):
    # At t=100, Person C enters forcefully (High Drama/Torque)
    if i == 100:
        K_AC = 3.0 # C exerts strong pull on A
        print(f"--- Time {t[i]:.1f}: Person C enters with high Torque ---")

    # Calculate Phase Differences
    dAB = thetaB[i] - thetaA[i]
    dAC = thetaC[i] - thetaA[i]

    # Update Phases (Kuramoto Dynamics)
    # A is pulled by both B and C
    thetaA[i+1] = thetaA[i] + (wA + K_AB*np.sin(dAB) + K_AC*np.sin(dAC)) * dt
    # B is only pulling A
    thetaB[i+1] = thetaB[i] + (wB + K_AB*np.sin(thetaA[i]-thetaB[i])) * dt
    # C is only pulling A
    thetaC[i+1] = thetaC[i] + (wC + K_AC*np.sin(thetaA[i]-thetaC[i])) * dt

    # Calculate Resonance Power between A and B (cos(delta_theta))
    # 1.0 = Max Resonance, lower is worse.
    resonance_AB[i+1] = np.cos(thetaA[i+1] - thetaB[i+1])

# --- Visualization ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot 1: Phase Evolution
ax1.set_title('The Three-Body Problem: Phase Evolution')
ax1.plot(t, thetaA, 'c', linewidth=2, label='Person A')
ax1.plot(t, thetaB, 'm', linewidth=2, label='Person B (Original Partner)')
ax1.plot(t, thetaC, 'y--', linewidth=1, alpha=0.6, label='Person C (Intruder)')
ax1.axvline(x=t[100], color='r', linestyle=':', label='C enters')
ax1.set_ylabel('Phase (Orientation)')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# Plot 2: A-B Resonance Power Collapse
ax2.set_title('Impact on A-B Connection (Resonance Power)')
ax2.plot(t, resonance_AB, 'g-', linewidth=3, label='A-B Resonance (cosΔθ)')
ax2.axvline(x=t[100], color='r', linestyle=':')
ax2.set_ylabel('Resonance Power (1.0=Max)')
ax2.set_xlabel('Time')
ax2.set_ylim(0, 1.1)
ax2.fill_between(t, resonance_AB, 0, color='green', alpha=0.1)
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
