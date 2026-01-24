# 🏗️ ARCHITECTURE.md — Resilient API Gateway

## 📖 Overview

This system consists of a **FastAPI Gateway Service** placed in front of a deliberately **Flaky Backend Service**.
The gateway implements key resilience patterns to protect upstream services and provide a stable client experience:

* ✅ **Circuit Breaker** (CLOSED → OPEN → HALF-OPEN)
* ✅ **Retry with Exponential Backoff**
* ✅ **Rate Limiting** (Sliding Window, per client/IP)
* ✅ **Observability** via `/health` and `/metrics`

---

## 🏛️ High-Level Components

### ✅ Gateway Service (FastAPI)

Responsibilities:

* Accept requests from clients
* Apply resilience patterns (rate limiting, circuit breaker, retries)
* Proxy requests to the backend (`/flaky-data`)
* Expose observability endpoints (`/health`, `/metrics`)

### ✅ Flaky Backend Service (FastAPI)

Responsibilities:

* Simulate real-world failures such as:

  * Successful responses
  * Random `503 Service Unavailable`
  * Random latency / timeouts

---
flowchart LR
    Client[Client] --> Gateway[API Gateway - FastAPI]
    Gateway --> Backend[Flaky Backend - FastAPI]

    Gateway --> RL[Rate Limiting]
    Gateway --> CB[Circuit Breaker]
    Gateway --> RT[Retry + Exponential Backoff]
    Gateway --> OBS[Health + Metrics]
---

## 🔁 Request Flow (End-to-End)

When a client calls:

* `GET /api/v1/data`

the gateway processes the request in this order:

1. **Rate Limiter**

   * Checks request count per client window
   * If exceeded → returns **429 Too Many Requests**

2. **Circuit Breaker**

   * If state is **OPEN** → fails fast and returns **503 Service Unavailable**
   * Prevents cascading failures and protects backend

3. **Retry + Exponential Backoff**

   * Calls backend endpoint
   * Retries only on transient errors:

     * backend `503`
     * request timeout / connection issues

4. **Response Returned**

   * If backend eventually succeeds → gateway returns **200**
   * If all retries fail → gateway returns **503**

---

## ⚡ Circuit Breaker

### ✅ States

| State         | Meaning                                          |
| ------------- | ------------------------------------------------ |
| **CLOSED**    | Normal operation, requests go to backend         |
| **OPEN**      | Backend considered unhealthy, gateway fails fast |
| **HALF-OPEN** | Limited test requests allowed to verify recovery |

### ✅ Transitions

* **CLOSED → OPEN**

  * Trigger: backend failures reach `FAILURE_THRESHOLD`

* **OPEN → HALF-OPEN**

  * Trigger: after `RECOVERY_TIMEOUT_SECONDS`

* **HALF-OPEN → CLOSED**

  * Trigger: test request succeeds

* **HALF-OPEN → OPEN**

  * Trigger: test request fails

### ✅ Why it matters

Circuit breakers prevent:

* Continuous retries hammering an already failing backend
* Increased latency
* Increased error rates across dependent services

---

## 🔄 Retry with Exponential Backoff

### ✅ Retry Conditions

Retries happen only for **transient failures**, such as:

* HTTP `503 Service Unavailable`
* Timeout / network issues

### ✅ Backoff Strategy

Example with exponential backoff:

* Attempt 1 → wait **0.5s**
* Attempt 2 → wait **1.0s**
* Attempt 3 → wait **2.0s**

Configured via:

* `MAX_RETRIES`
* `INITIAL_BACKOFF_SECONDS`
* `BACKOFF_MULTIPLIER`

### ✅ Why it matters

Retry helps recover from:

* temporary backend failures
* short-lived overload
* slow network spikes

---

## 🚦 Rate Limiting (Sliding Window)

### ✅ Behavior

* Rate limiting is applied per client (typically IP-based)
* Uses a **sliding window approach** (not fixed buckets)

### ✅ Result

* Allowed → request continues normally
* Blocked → gateway returns:

```http
429 Too Many Requests
```

Configured via:

* `RATE_LIMIT_ENABLED`
* `RATE_LIMIT_REQUESTS_PER_WINDOW`
* `RATE_LIMIT_WINDOW_SECONDS`

### ✅ Why it matters

Rate limiting prevents:

* backend overload
* denial-of-service-like request bursts
* unfair consumption by a single client

---

## 📊 Observability

### ✅ Health Endpoint

Gateway exposes:

* `GET /health`

Example response:

```json
{"status":"ok"}
```

### ✅ Metrics Endpoint

Gateway exposes:

* `GET /metrics`

Example response:

```json
{
  "circuit_breaker_state": "OPEN",
  "total_retries": 6,
  "rate_limit_allowed": 5,
  "rate_limit_blocked": 10
}
```

---

## 🐳 Deployment (Docker Compose)

### ✅ Services

Docker Compose starts:

* Gateway service container
* Flaky backend container

### ✅ Build and Start

```bash
docker-compose up --build -d
```

### ✅ Stop Services

```bash
docker-compose down
```

---

## ✅ Verification & Testing

### ✅ Run Verification Script

```bash
./verify.sh
```

### ✅ Run All Tests

```bash
docker-compose exec gateway pytest tests -v
```

---
