#!/bin/bash

# =====================================================================
# Local Repository Workflow Verification and Testing Harness
# =====================================================================

set -e

# Visual text attributes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}=========================================================================${NC}"
echo -e "${CYAN}   RUNNING LOCAL INTEGRATION WORKFLOW SUITE FOR ENVIRONMENT LOGS         ${NC}"
echo -e "${CYAN}=========================================================================${NC}"

# Step 1: Run the new Fibrinolysis and Schema Compliance Verification rules
echo -e "\n[STEP 1/3]: Executing automated YAML configuration schema verifications..."
python3 src/fibrinolysis_verifier_core.py
echo -e "${GREEN} -> Schema check and lytic transformation assertions passed successfully.${NC}"

# Step 2: Execute the Upper and Lower Respiratory Reflex Engines
echo -e "\n[STEP 2/3]: Running fluid advection reflex jet mechanical assertions..."
python3 src/respiratory_reflex_engine.py
echo -e "${GREEN} -> Gag, sneeze, and airway cough jet velocity equations verified.${NC}"

# Step 3: Run the new Laplace Pulmonary Alveolar Collapse Engine
echo -e "\n[STEP 3/3]: Running Laplace Law modified structural atelectasis tests..."
python3 src/pulmonary_collapse_engine.py
echo -e "${GREEN} -> Covalent bond surfactant decay loop and collapse ODEs verified.${NC}"

echo -e "\n${GREEN}=========================================================================${NC}"
echo -e "${GREEN} ✅ ALL LOCAL ENVIRONMENT WORKFLOW COMMANDS PASSED STRUCTURAL VERIFICATION ${NC}"
echo -e "${GREEN}=========================================================================${NC}"
