#!/bin/bash
set -e

echo "--- Starting Lab 1 Grading ---"

# 1. Перевірка чи запущено контейнер з назвою 'app'
if [ $(docker ps -q -f name=app | wc -l) -eq 0 ]; then
  echo "❌ Error: Container named 'app' not found."
  exit 1
fi

# 2. Перевірка Health Check (200)
echo "Step 1: Checking /health (Expect 200)..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" localhost:8080/health)
if [ "$STATUS" -ne 200 ]; then
  echo "❌ Error: Expected 200, but got $STATUS"
  exit 1
fi

# 3. Перевірка формату JSON
echo "Step 2: Checking JSON logs..."
docker logs app --tail 5 \
  | while read -r line; do
      JSON=$(echo "$line" | sed -n 's/.*\({.*}\)/\1/p')
      if [ -n "$JSON" ]; then
          echo "$JSON" | jq . > /dev/null 2>&1
          if [ $? -ne 0 ]; then
              echo "❌ Error: Logs are not valid JSON."
              exit 1
          fi
      fi
  done

# 4. Тест на стійкість (Resilience)
echo "Step 3: Stopping DB to check 503 error..."
DB_CONTAINER=$(docker compose ps -q db)
docker stop $DB_CONTAINER > /dev/null
sleep 3
STATUS_503=$(curl -s -o /dev/null -w "%{http_code}" localhost:8080/health)
if [ "$STATUS_503" -ne 503 ]; then
  echo "❌ Error: App must return 503 when DB is offline."
  docker start $DB_CONTAINER
  exit 1
fi

docker start $DB_CONTAINER > /dev/null
echo "✅ SUCCESS: Lab 1 is passed!"