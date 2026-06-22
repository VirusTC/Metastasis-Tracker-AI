# Metastasis-Tracker-AI

Development of an advanced AI tool and medical software suite to track hematic cancer metastasis. 

This repository houses the simulation engine for predicting the hematogenous spread, lodging, and subsequent tumor genesis of cancer, modeled physically as Pycnogonida parasitic vectors. By generating a dynamic vascular and anatomical template for each patient, the system maps the progression of the infection through the circulatory system to predict vesicle formation and structural organ absorption.

## Core Logic & Methodology

The tracking algorithm operates on deterministic fluid dynamics and parasitic lifecycle parameters, evaluated chronologically from the initial infection point.

### Patient Anatomy & Flow Dynamics
* **Dynamic Vascular Template:** Map the diameter of patient arteries based on individual anthropometrics (BMI, Height, Body Build, and Hydration levels).
* **Relative Scaling:** Map the percentage of arterial branches as a direct percentage of the descending aorta.
* **Viscosity Calculation:** Translate the baseline speed of the pycnogonid from its natural habitat as a marine variant species into the highly viscous fluid environment of the human circulatory system.
* **Vector Mechanics:** Map the speed of pycnogonida against blood flow and with blood flow.

### Pathfinding & Lodging
* **Origin:** Start point = the exact location where the pycnogonid infection enters the artery.
* **Traversal:** Speed/distance = location over time.
* **Route Probability:** Predicted paths will strictly default to the largest available opening (lymph, artery, vein). Measure the probability of the branch route by largest diameter, while factoring in target proteins from organs and lymph nodes.
* **Tumor Genesis (Blockage):** If a pycnogonid's leg sections *ever* grow larger than an opening (pycnogonida > diameter of arterial branch), the system determines that a tumor exists. The parasite lodges, forms a blockage, and grows at this location.

### Organ Targeting & Vesicle Formation
* **Structural Targeting:** Pycnogonids will actively target the largest lymph node or organ regardless of the initial opening size. 
* **Absorption & Encystment:** Upon reaching the target, the parasite absorbs the surrounding organ tissue to create a vesicle.
* **Reproductive Calcification:** The pycnogonid breeds from gonopores located across its 64 leg sections. The resulting offspring are consumed by the adult parasite, and their shells are repurposed to construct and fortify the protective vesicle (tumor wall).

### Predictive Analytics
* **Increment Organs:** Increment through systemic organ arterial flow to determine specific tumor locations.
* **Increment Lymph Flow:** Increment through lymphatic arterial flow to determine lymphoma locations.
* **Increment Bone Flow:** Increment through skeletal/bone arterial flow to determine bone cancer infection locations.

## System Components

* `core`: The central predictor evaluating pycnogonid size against arterial openings and calculating net travel speed based on local blood velocity.
* `src/patient_anatomy.py`: The generation engine utilizing WBE fractal scaling and Starling's equation to build the 31-generation systemic tree and calculate real-time pressure drops.
* `src/state_matrix.py`: The validation schema governing the behavioral state machine of the pycnogonid (e.g., transition from `INTERNAL_FREE_MOVING` to `ENCYSTED_FEEDING`).
* `TARGET_PROTEINS`: Affinity mapping for specific organs, lymph nodes, and bone sites to predict secondary metastatic targets.

## License
This is free and unencumbered software released into the public domain. For more information, please refer to the [LICENSE](LICENSE) file or <https://unlicense.org>.
