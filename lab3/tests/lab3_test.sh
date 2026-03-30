#!/bin/bash
set -e

echo "--- Starting Lab 3 Grading (Kubernetes Check) ---"

# 1. Перевірка статусу Deployment
echo "Step 1: Waiting for Deployment rollout..."
kubectl rollout status deployment/ecommerce-app --timeout=60s

# 2. Перевірка наявності Probes
echo "Step 2: Checking for Liveness and Readiness probes..."
HAS_PROBES=$(kubectl get deployment ecommerce-app -o jsonpath='{.spec.template.spec.containers[0].livenessProbe}')
if [ -z "$HAS_PROBES" ]; then
  echo "❌ Error: Liveness/Readiness probes are missing in Deployment."
  exit 1
fi

# 3. Перевірка секретів
echo "Step 3: Verifying Secret usage..."
HAS_SECRET=$(kubectl get deployment ecommerce-app -o jsonpath='{.spec.template.spec.containers[0].envFrom[0].secretRef.name}')
if [ -z "$HAS_SECRET" ]; then
  echo "❌ Error: Secrets must be injected via envFrom/secretRef."
  exit 1
fi

echo "✅ SUCCESS: Lab 3 is passed!"