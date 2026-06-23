# Macrophage Consumption and Splenic Unclogging Specifications

## 1. Overview
This module defines the kinetic and metabolic parameters governing the removal of mechanically trapped elements, such as circulating tumor cells (CTCs) or cellular fragments, from the interendothelial slits of the splenic red pulp sinuses.

---

## 2. Mathematical Formulations

### A. Macrophage Mass-Balance Consumption Model
The accumulation and structural clearance of trapped particles ($M_{\text{splenic\_load}}$, mg) inside the splenic filter network follow non-linear Michaelis-Menten consumption kinetics:

$$\frac{dM_{\text{splenic\_load}}(t)}{dt} = J_{\text{entrapment}}(t) - V_{\text{phago}}(t)$$

### B. Environmental pH and Activation Multipliers
The biological mass-clearance rate ($V_{\text{phago}}$, mg/s) is coupled directly to the localized tissue pH matrix. Severe local lactic acidosis causes conformational and functional macro-phage suppression ($\eta_{\text{activation}}$), creating an obstacle that slows down the unclogging timeline:

$$V_{\text{phago}}(t) = \eta_{\text{activation}}(\text{pH}) \times \left( \frac{V_{\text{max\_phago}} \cdot M_{\text{splenic\_load}}(t)}{K_{\text{m\_splenic}} + M_{\text{splenic\_load}}(t)} \right) \times \chi$$

Where $\eta_{\text{activation}}(\text{pH}) \to 0.15$ if environmental conditions plunge below normal homeostatic boundaries ($pH < 7.10$).

---

## 3. Storage Optimization & Makefile Automation

Continuous operations generate large binary datasets. The ecosystem automates file cleanup and directory testing routines via unified console shortcuts:

*   **Log Compression**: Loose `.medbin` telemetry tracking arrays are packed into compressed ZIP containers and moved to the `archive/` folder via:
    ```bash
    make archive
    ```
*   **Harness Execution**: The complete multi-module simulation pipeline is checked, verified, and run using short shortcut sequences:
    ```bash
    make run-ui    # Launches live streaming visualization tables
    make parse     # Direct terminal translation of binary logs
    ```
