#!/bin/bash
# Lecturer's Master Validation Script for Lab 2
set -e

OWNER_LC=$(echo "${GITHUB_REPOSITORY_OWNER}" | tr '[:upper:]' '[:lower:]')
PACKAGE_NAME="ecommerce-app"

echo "--- Starting Lab 2 Grading (GHCR Check) ---"

# 1. Checking package presence via GitHub API
echo "Step 1: Requesting package metadata from GHCR..."
RESPONSE=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/users/${GITHUB_REPOSITORY_OWNER}/packages/container/${PACKAGE_NAME}")

if echo "$RESPONSE" | grep -q "Not Found"; then
  echo "❌ Error: Package '${PACKAGE_NAME}' not found in GHCR."
  echo "Make sure your image name is: ghcr.io/${OWNER_LC}/${PACKAGE_NAME}"
  exit 1
fi

# 2. Verifying Tags (latest + SHA)
echo "Step 2: Verifying tags..."
VERSIONS=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/users/${GITHUB_REPOSITORY_OWNER}/packages/container/${PACKAGE_NAME}/versions")

TAGS=$(echo "$VERSIONS" | jq -r '.[]?.metadata?.container?.tags[]?' )

if [[ ! "$TAGS" =~ "latest" ]]; then
  echo "❌ Error: 'latest' tag is missing."
  exit 1
fi

if [[ ! "$TAGS" =~ "sha-" ]]; then
  echo "❌ Error: Git SHA tag (sha-xxxxxxx) is missing."
  exit 1
fi

echo "✅ SUCCESS: Lab 2 is passed!"