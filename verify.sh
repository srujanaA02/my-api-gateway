#!/bin/bash
set -e

echo "🔧 Building and starting containers..."
docker-compose up --build -d

sleep 3

echo "🩺 Checking health endpoints..."
echo "Gateway health: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)"
echo "Flaky backend: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/flaky-data)"

echo "📜 Checking gateway logs for resilience events..."
docker-compose logs gateway | grep -E "CircuitBreaker|Retry|RateLimiter" || echo "No resilience logs found yet."

echo "📊 Generating traffic to populate metrics..."
for i in {1..15}; do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/api/v1/data
done

echo "📊 Saving metrics snapshot..."
curl -s http://localhost:8000/metrics | python -m json.tool > metrics.json
cat metrics.json

echo "🧪 Running all tests..."
docker-compose exec gateway pytest tests -v

echo "✅ Verification complete — metrics.json updated with current gateway stats"
