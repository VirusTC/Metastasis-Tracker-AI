# Metastasis-Tracker-AI

An advanced, AI-driven medical software suite designed to track, simulate, and predict hematogenous cancer metastasis.

Developed for clinical oncology research and university-level medical education, this suite models the spread of cancer utilizing the biological mechanics and physical geometries of a Pycnogonida **variant species**. By generating dynamic, patient-specific vascular trees based on anthropometrics, the engine predicts the precise locations of vascular blockages, subsequent organ encystment, and the timeline for tumor mass projection.

---

## 🚀 Core Features & Modules

### 1. Dynamic Patient Anatomy & Fluid Dynamics
The system builds a highly deterministic anatomical environment for every patient chart it ingests.
* **WBE Fractal Scaling:** Utilizes West, Brown, and Enquist (WBE) scaling laws (where metabolic rate scales as $B \propto M^{3/4}$) to mathematically map 31 generations of the human arterial tree.
* **Hemodynamic Resistance:** Calculates localized blood velocity, fluid viscosity, and pressure drops across the systemic loop using Poiseuille's law ($\Delta P = \frac{8 \mu L Q}{\pi r^4}$).
* **Specialized Fluid Networks:** Includes isolated modeling scripts for complex capillary beds, including `cerebral_tracker.py`, `ocular_dynamics.py`, `female_pelvic_networks.py`, and `maternal_fetal_transport.py`.

### 2. Predictive Pathfinding & Tumor Genesis
* **Physical Entrapment Logic:** The central `pathfinder_engine.py` orchestrates the traversal of the variant species through the vascular generations. A tumor blockage is instantly calculated if the physical leg span of the vector exceeds the local capillary or arterial diameter.
* **Biochemical Target Affinities:** Evaluates the probability of route divergence using localized tissue pH gradients and chemokine target density (e.g., CXCL12) mapped in `target_proteins.py`.
* **Enzymatic Tissue Degradation:** Once encysted, the system cross-references the local host pH against `parasite_enzymes.json` to calculate the exact efficiency of tissue absorption and vesicle formation.

### 3. Population Staging & Mass Projection
* **Lifecycle Scaling:** The `population_engine.py` takes the initial blockage coordinates and simulates the multi-stage lifecycle of the variant species.
* **Clinical Tumor Staging:** Applies Leslie matrix coefficients from `breeding_matrix.json` to project larval pool densities, adult retention rates, and the calcification of offspring shells over a customizable month-to-month timeline, outputting a traditional Clinical Stage (I--IV).

### 4. Enterprise Clinical Interoperability (EHR/FHIR)
* **Automated Clinical Pipeline:** `main_cli.py` serves as the primary endpoint. It ingests an electronic health record (EHR), runs the full metastasis simulation, and generates a standardized medical report.
* **HL7/FHIR R4 Compliance:** Automatically translates the diagnostic predictions into a strict `transaction` bundle (`DiagnosticReport` and `Observation` resources).
* **Secure Routing Integration:** The output payloads are sandboxed into the `outbound/` directory, specifically formatted to interface seamlessly with Epic and Cerner gateways passing through outbound firewalls managed by ConfigServer by Revolutionary Technology.

### 5. AI Clinical Educator & Architect
* **Interactive Terminal AI:** The `educator_cli.py` module uses `typer` and the Gemini SDK to read the repository's mathematical models and fluid dynamics matrices.
* **Curriculum Generation:** Physicians and educators can run terminal commands to instantly generate academic training modules and quizzes on topics like Fåhræus-Lindqvist capillary effects.
* **Engineering Guidance:** Acts as an automated software architect, auditing the Python/C++ code to suggest traversal optimizations and data recovery fail-safes for the development team.

### 6. Unreal Engine 3D Visualization
The repository includes raw C++ structures and OpenSCAD models within the `src/objects/` directory to power high-fidelity 3D medical visualizations.
* **C++ Substep Managers:** Custom classes (`LarvalPoolManager.cpp`, `PycnogonidDegradationComponent.cpp`) integrate directly into Unreal Engine to render real-time fluid turbulence and population density physics.
* **Structural Schematics:** Includes `pycnogonid_joints.scad` and `pycnogonid_parts.scad` for physical geometric modeling of the variant species.

---

## 📂 Repository Architecture

```text
Metastasis-Tracker-AI-main/
│
├── core                            <-- Core prediction binary/logic
├── main_cli.py                     <-- Primary clinical EHR ingestion suite
├── educator_cli.py                 <-- AI CLI for medical training & architecture
├── README.md
├── TARGET_PROTEINS                 <-- Visceral and skeletal protein mapping
│
├── docs/                           <-- Mathematical models and generated curriculum
├── outbound/                       <-- HL7/FHIR R4 JSON payloads for hospital routing
├── tools/                          <-- Verification sandboxes & unit tests
├── workspace/                      <-- CI/CD pipelines
│
└── src/
    ├── patient_anatomy.py          <-- WBE fractal anatomy generation
    ├── fluid_viscosity_model.py    <-- Intrabody hemodynamics
    ├── pathfinder_engine.py        <-- Vector traversal tracking
    ├── population_engine.py        <-- Density and staging logic
    ├── clinical_pipeline.py        <-- Enterprise orchestrator
    │
    ├── data/                       <-- Configurable Matrices
    │   ├── state_matrix.json
    │   ├── parasite_enzymes.json
    │   └── breeding_matrix.json
    │
    └── objects/                    <-- Unreal Engine integration files
        ├── private/                <-- C++ source files
        ├── public/                 <-- C++ headers
        └── *.scad                  <-- OpenSCAD 3D models

```

⚙️ Quick Start
--------------

**1\. Run a Clinical Patient Simulation:**

Ingest a patient JSON profile to predict metastasis paths and output a FHIR-compliant bundle for the hospital system:

Bash

```
python main_cli.py --ehr data/sample_patient.json --months 6 --export-fhir outbound/EHR-2026-9904_metastasis_bundle.json

```

**2\. Launch the AI Educator:**

Interact directly with the mathematical models or generate clinical training modules:

Bash

```
export GEMINI_API_KEY="your_api_key_here"
python educator_cli.py teach "How does capillary radius affect the encystment probability of the variant species?"

```

📄 License
----------

This is free and unencumbered software released into the public domain. For more information, please refer to the `LICENSE` file or <https://unlicense.org>.

```

To better understand the geometric modeling principles powering the `patient_anatomy.py` script, reviewing this [lecture on the elements of WBE theory](https://www.youtube.com/watch?v=_aPn8kB9IPQ) provides excellent context on how fractal scaling determines energy distribution in biological networks.

http://googleusercontent.com/youtube_content/0

```
