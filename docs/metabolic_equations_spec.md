# Metabolic Kinetics and Enzymatic Velocity Specifications (`docs/metabolic_equations_spec.md`)

## 1. Overview
This technical standard defines the bioenergetic and enzymatic velocity profiles governing homeostatic buffering transformations. It maps the integration of multi-substrate Carbonic Anhydrase conversion rates, Henderson-Hasselbalch bicarbonate balances, and inotropic myocardial force alterations under extreme metabolic stress or sepsis.

---

## 2. Structural Mathematical Formulations

### A. Accelerated Carbonic Anhydrase (CA) Kinetic Velocity
The hydration velocity of carbon dioxide (\(V_{\text{hydration}}\), mmol/L/s) within plasma border surfaces scales via an accelerated Michaelis-Menten formulation coupled to a non-linear enzyme denaturation efficiency parameter (\(\eta_{\text{CA}}\)):

\[V_{\text{hydration}} = \eta_{\text{CA}}(\text{pH}) \cdot K_{\text{accel}} \cdot \left( \frac{V_{\text{max\_CA}} \cdot [CO_2]}{K_{m\text{\_CO2}} + [CO_2]} \right) - V_{\text{dehydration\_back\_flux}}\]

Where \(K_{\text{accel}} = 18500.0\). Proton-induced conformational denaturation drops active enzyme efficiency when structural pH boundaries break down:

\[\eta_{\text{CA}}(\text{pH}) = \max \left( 0.05, \, \frac{1.0}{1.0 + e^{-8.5 \cdot (\text{pH} - 6.80)}} \right)\]

### B. Carbonic Acid-Bicarbonate Buffer Equilibrium
Systemic hydrogen proton accumulation generated during anaerobic lactic acid spikes (\(HLac\)) is neutralized stoichiometrically by circulating plasma bicarbonate (\(HCO_3^-\)). Terminal blood pH shifts tracking across execution cycles resolve via:

\[\text{pH}(t) = 6.10 + \log_{10} \left( \frac{[HCO_3^-](t)}{0.03 \cdot PCO_2(t)} \right)\]

### C. Myocardial Force Scaling & Calcium Rigor
Serum calcium extraction (\([Ca^{2+}]_{\text{serum}}\)) increases cross-bridge troponin binding potential (positive inotropy). However, extreme structural thresholds override this vector, inducing diastolic relaxation failure and muscle contracture rigor (\(\Phi_{\text{lusitropy}}\)):

\[F_{\text{myo}} = F_{\text{baseline}} \times \left( \frac{[Ca^{2+}]_{\text{serum}}^{2.2}}{[Ca^{2+}]_{\text{serum}}^{2.2} + 9.5^{2.2}} \right) \times \Phi_{\text{lusitropy}}\]

\[\Phi_{\text{lusitropy}} = \max \left( 0.1, \, 1.0 - 0.04 \cdot \max\left(0.0, \, [Ca^{2+}]_{\text{serum}} - 14.0\right)^2 \right)\]

---

## 3. Platform Boundary Class Conditions

The environment categorizes active cardiac mechanical performance states into three discrete tracking classes:
1.  **NORMAL_CONTRACTILITY**: Homeostatic baseline operational limits secure.
2.  **HYPERDYNAMIC_INOTROPY**: Serum calcium is elevated (\(> 11.5\text{ mg/dL}\)), increasing localized stroke volume outputs.
3.  **CALCIUM_RIGOR_CONTRACTURE**: Critical metabolic emergency (\([Ca^{2+}]_{\text{serum}} > 14.0\text{ mg/dL}\)). Lusitropy collapses, forcing severe myofibrillar muscle contracture and restricting net mechanical output.

---

## 4. Standalone Ingestion Script Template

To initialize and parse these bioenergetic properties from your master tracking loops, call the module classes using this unified design configuration framework:

```python
from src.metabolic_dashboard_engine import AdvancedMetabolicKineticEngine

# Initialize the calculator profile
kinetic_model = AdvancedMetabolicKineticEngine(hydration_level=1.0)

# Run a real-time evaluation at a strained tissue boundary point (pH: 7.02)
report = kinetic_model.calculate_ca_velocity_efficiency(current_ph=7.02, co2_mmol_L=2.4)

print(f"Catalytic Efficiency:  {report['enzyme_efficiency_coefficient'] * 100}%")
print(f"Hydration Conversion:  {report['instantaneous_hydration_velocity_mmol_L_s']} mmol/L/s")
print(f"Structural State Status: {report['catalytic_state']}")
```
