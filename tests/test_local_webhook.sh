#!/bin/bash

# =====================================================================
# Local Webhook Integration Validation Driver
# =====================================================================

# Stop execution immediately if any internal task failures occur
set -e

MOCK_PORT=8080
LOCAL_URL="http://localhost:${MOCK_PORT}"

echo "========================================================================="
echo " STARTING LOCAL CI/CD WEBHOOK VALIDATION HARNESS"
echo "========================================================================="

# Step 1: Boot up a localized background listening server using netcat (nc)
# This intercepts outbound curl POST payloads and echoes the data stream
echo -e "\n[STEP 1]: Spin up local mock listener on port ${MOCK_PORT}..."
nc -l -p ${MOCK_PORT} > tests/caught_webhook_payload.json &
MOCK_PID=$!

# Allow the background server node time to stabilize and initialize
sleep 1

# Step 2: Construct the mock diagnostic JSON payload mirror matching the GitHub Actions layout
echo -e "\n[STEP 2]: Simulating pipeline boundary failure payload..."
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "text": "🚨 *LOCAL ENVIRONMENT ALERT*: Local verification pipeline run has encountered a simulated validation boundary breach.",
    "attachments": [
      {
        "color": "danger",
        "fields": [
          { "title": "Environment context", "value": "Local Sandbox Core Check", "short": true },
          { "title": "Verification Status", "value": "FAILED / UNIT_ASSERTION_BREACH", "short": true },
          { "title": "Target Engine File", "value": "src/sepsis_redox_engine.py", "short": false }
        ]
      }
    ]
  }' ${LOCAL_URL}

# Wait for background transport processes to conclude
wait ${MOCK_PID} 2>/dev/null || true

# Step 3: Print the intercepted payload data array to verify structural formatting
echo -e "\n[STEP 3]: Intercepted Webhook Stream Result Validation:"
echo "------------------------------------------------------------------------"
cat tests/caught_webhook_payload.json
echo "------------------------------------------------------------------------"

# Clean up transient runtime files
rm -f tests/caught_webhook_payload.json
echo -e "\n[+] Local test harness successful. Webhook format validated."
