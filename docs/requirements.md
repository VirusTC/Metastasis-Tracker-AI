Based on the comprehensive file architecture of the `metastasis-tracker-ai` repository---including the newly integrated HPC Multicore/CUDA pipelines, the AI Educator CLI, the HDF5 pulmonary cores, and the YAML testing environments---here is the complete `requirements.txt` for your engineering team.

This file is organized by subsystem so your deployment pipelines (and the Univac-IX bridge environment) can cleanly track dependencies.

### `requirements.txt`

### ⚙️ Installation Instructions for the Team

**For Local Development / Verification Sandboxes:**

Your team can install the entire suite into their virtual environments using:

Bash

```
pip install -r requirements.txt

```

**For the Enterprise CentOS/AlmaLinux Servers (HPC & Univac-IX):**

Because your system relies heavily on `numba` for NVIDIA GPU delegation and Multicore JIT compiling, ensure the production server environment has the underlying CUDA toolkit installed at the system level. If you are using Conda for your server environments, you can ensure strict GPU hardware binding by running:

Bash

```
conda install --file requirements.txt
conda install cudatoolkit

```
