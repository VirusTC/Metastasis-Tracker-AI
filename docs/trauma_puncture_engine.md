# Trauma and Puncture Engine Technical Specification (`src/trauma_fluid_core.py`)

## 1. Overview
The Trauma Engine handles the programmatic conversion of microscopic contact forces into directional point stress configurations. It evaluates when an object with known sharpness thresholds will cause mechanical puncture, organ rupture, or cascading vascular hemorrhages across the 31 vascular generations and specialized organ systems.

---

## 2. Mathematical Architecture

### A. Point Puncture Stress Equation
Whenever an anomaly node contacts a target boundary layer, localized point stress (\(\sigma_{\text{local}}\)) is calculated based on the radius of curvature of the contact tip (\(A_{\text{tip}}\)):

\[\sigma_{\text{local}} = \frac{F_{\text{contact}}}{A_{\text{tip}}} \quad \left(\text{Pascals or N/m}^2\right)\]

Where \(A_{\text{tip}} = \pi \cdot r_{\text{tip}}^2\). As the radius of curvature approaches micro-scale limits, the stress amplification factor spikes exponentially.

### B. Material Yield Failure Condition
A rupture or fluid hemorrhage alert is committed to the tracking logs when the applied stress passes the defined material yield boundaries (\(\sigma_{\text{uts}}\)) of the compartment:

\[\text{Boundary Status} = \begin{cases} \text{INTACT}, & \text{if } \sigma_{\text{local}} \le \sigma_{\text{uts\_tissue}} \\ \text{CRITICAL\_HEMORRHAGE}, & \text{if } \sigma_{\text{local}} > \sigma_{\text{uts\_tissue}} \end{cases}\]

### C. Reference Material Capacities
*   **Brain Neural Matrix**: 0.03 MPa (Minimum resistance; high viscoelastic layout fragility)
*   **Capillary / Venous Wall**: 1.10 MPa
*   **Macro Artery Core Trunk**: 2.80 MPa
*   **Cortical Bone Grid**: 135.00 MPa (Maximum structural density boundary)

---

## 3. Active Hemorrhage Cascade Model

Once a puncture has occurred, the engine activates a time-series leakage simulation using the Torricelli-Poiseuille orifice formulation:

\[Q_{\text{hem}}(t) = C_d \cdot A_{\text{lesion}} \cdot \sqrt{\frac{2 \cdot \Delta P(t)}{\rho_{\text{blood}}}}\]

Vascular backpressures decay exponentially as blood leaves the system, automatically scaling down the leakage velocity over time until it achieves hydrostatic equilibrium with the interstitial space (\(P_{\text{vessel}} \to P_{\text{interstitial}}\)).

---

## 4. Platform Integration Protocol

To deploy this module inside your structural simulation loop, import the core engine and execute the calculation directly alongside your tracking state vectors:

```python
from src.trauma_fluid_core import VascularHemorrhageDynamicsEngine

# 1. Instantiate the tracker with a 3.5-micron tip profile
trauma_engine = VascularHemorrhageDynamicsEngine(tip_radius_microns=3.5)

# 2. Check for dynamic fluid bleeding cascade over 30 seconds
bleeding_report = trauma_engine.simulate_active_bleeding_cascade(
    initial_p_vessel_mmHg=90.0, 
    p_interstitial_mmHg=4.0, 
    time_steps_sec=30
)

print(f"Total Projected Fluid Loss: {bleeding_report['total_cumulative_blood_loss_mL']} mL")
```
