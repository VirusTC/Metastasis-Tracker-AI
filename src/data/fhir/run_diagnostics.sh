#!/bin/bash

# =====================================================================
# Real-Time Telemetry Spreadsheet Profiler Interface
# =====================================================================

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}[*] Starting real-time spreadsheet parsing and diagnostic scans...${NC}"

# Execute python diagnostic module and capture the boolean return status directly
if python3 -c "from src.data.fhir.csv_diagnostics import CSVDiagnosticsAndRetentionEngine; d=CSVDiagnosticsAndRetentionEngine(); exit_code = 0 if d.execute_spreadsheet_anomaly_check() else 1; exit(exit_code)"; then
    echo -e "${GREEN}✅ SUCCESS: Spreadsheet checked out clean. Continuous ingestion secure.${NC}"
    exit 0
else
    echo -e "${RED}❌ FAILURE: Ingestion stopped. Outliers or schema corruption detected inside file.${NC}"
    exit 1
fi
