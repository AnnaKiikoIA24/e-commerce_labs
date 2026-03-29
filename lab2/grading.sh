#!/bin/bash
set -e

IMAGE=ghcr.io/${GITHUB_REPOSITORY_OWNER}/ecommerce-app:sha-${GITHUB_SHA}

echo "Running container to test /health..."

docker run --rm -d --name test_app -p 8081:8080 $IMAGE

sleep 5

HEALTH=$(curl -s http://localhost:8081/health | jq -r '.status')

docker stop test_app

# Грейдінг
if [ "$HEALTH" == "ok" ]; then
  echo "Grading passed ✅"
  exit 0
else
  echo "Grading failed ❌"
  exit 1
fi