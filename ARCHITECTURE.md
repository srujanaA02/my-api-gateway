# 🏗️ ARCHITECTURE.md — Resilient API Gateway

## 📖 Overview
A FastAPI **Gateway Service** sits in front of a **Flaky Backend** and applies resilience patterns:
* Circuit Breaker (CLOSED → OPEN → HALF-OPEN)
* Retry with Exponential Backoff
* Rate Limiting (Sliding Window)
* Observability via `/health` and `/metrics`

---

## 🔁 Request Flow
1. **Rate Limiter** → reject excess requests (`429`)
2. **Circuit Breaker** → fail fast if OPEN (`503`)
3. **Retry** → call backend, retry on `503/timeout` with backoff
4. **Response** → return final result to client

---

## ⚡ Circuit Breaker

* **CLOSED** → normal, all requests pass
* **OPEN** → backend unhealthy, fail fast
* **HALF-OPEN** → limited test requests

**Transitions:** * CLOSED → OPEN → after `FAILURE_THRESHOLD` failures
* OPEN → HALF-OPEN → after `RECOVERY_TIMEOUT_SECONDS`
* HALF-OPEN → CLOSED (success) / OPEN (failure)

---

## 🔄 Retry
* Handles transient errors (`503`, timeouts)
* Exponential backoff: 0.5s → 1.0s → 2.0s
* Config: `MAX_RETRIES`, `INITIAL_BACKOFF_SECONDS`, `BACKOFF_MULTIPLIER`

---

## 🚦 Rate Limiting
* Sliding window per client (IP)
* Allowed → pass, Excess → `429`
* Config: `RATE_LIMIT_ENABLED`, `RATE_LIMIT_REQUESTS_PER_WINDOW`, `RATE_LIMIT_WINDOW_SECONDS`

---

## 📊 Observability
* **`/health`** → `{"status":"ok"}`
* **`/metrics`** → JSON snapshot of circuit breaker state, retries, and rate limit stats

```json
{
  "circuit_breaker_state": "OPEN",
  "total_retries": 6,
  "rate_limit_allowed": 5,
  "rate_limit_blocked": 10
}

---

## 🐳 Deployment
Use Docker Compose to build and orchestrate the Gateway and Flaky Backend services in an isolated environment.

**Build and Start:**
```bash
docker-compose up --build -d


## ✅ Verify & Run Tests

**Verify:**
```bash
./verify.sh

**Run All Tests:**
```bash
docker-compose exec gateway pytest tests -v

---
