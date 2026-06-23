#!/usr/bin/env bash

# ==============================================================================
# 🤖 HEADLESS COMPILE & AUTOMATION TOOL PASS RUNNER
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration Paths ---
PROJECT_NAME="MetastasisTrackerAI"
PLATFORM="Linux"
CONFIG="Development"
UE_ROOT="/workspace/UnrealEngine" # Adjust this to your absolute UE engine root path
PROJECT_PATH="/workspace/Metastasis-Tracker-AI/MetastasisTrackerAI.uproject"
REPORT_DIR="/workspace/Metastasis-Tracker-AI/Saved/AutomationReports"

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

echo "====================================================="
echo "⚙️  STEP 1: Compiling C++ Subsystems via UnrealBuildTool..."
echo "====================================================="

# Execute hard link pass compiler via UBT command line
"$UE_ROOT/Engine/Build/BatchFiles/RunUBT.sh" \
    "$PROJECT_NAME" \
    "$PLATFORM" \
    "$CONFIG" \
    -Project="$PROJECT_PATH" \
    -NoHotReload \
    -Progress

echo "✅ Compilation successful!"
echo ""
echo "====================================================="
echo "🧪 STEP 2: Running Automated Test Suites via AutomationTool..."
echo "====================================================="

# Run headless tests. We isolate your specific custom classes using the filter 
# flag to skip standard engine test suites.
"$UE_ROOT/Engine/Build/BatchFiles/RunUAT.sh" RunUnreal \
    -project="$PROJECT_PATH" \
    -platform="$PLATFORM" \
    -configuration="$CONFIG" \
    -build \
    -run \
    -unattended \
    -nopause \
    -nullrhi \
    -ExecCmds="Automation RunTests Pycnogonid; Quit" \
    -ReportOutputPath="$REPORT_DIR"

# Check if reports were generated successfully
if [ -f "$REPORT_DIR/index.json" ]; then
    echo "✅ Automation testing pass completed!"
    echo "📊 Test report saved to: $REPORT_DIR/index.json"
else
    echo "⚠️  Testing finished, but no structural JSON report index was discovered."
fi

echo "====================================================="
echo "🚀 Pipeline execution completed successfully!"
echo "====================================================="
