# 🚀 Resilient API Gateway with Flaky Backend

## 📖 Overview
This project implements a **robust API Gateway** that sits in front of a deliberately **flaky backend service**.  
The gateway applies advanced **resilience patterns** to ensure stability and fault tolerance in distributed systems:

- **Circuit Breaker**: Prevents cascading failures by halting calls to a failing service.
- **Retry Mechanism**: Handles transient errors with configurable retries and exponential backoff.
- **Rate Limiting**: Protects the backend from overload by restricting client requests.
- **Observability**: Provides `/health` and `/metrics` endpoints for monitoring.

This project simulates real‑world scenarios where resilience is critical for cloud‑native and microservices architectures.

---

## 🛠️ Requirements
To run this project locally (without Docker), you need:

- Python 3.11+
- Pip (Python package manager)

Install dependencies from `requirements.txt`:

```bash
pip install -r gateway_service/requirements.txt
pip install -r flaky_service/requirements.txt
---

## 🏗️ Architecture
The solution consists of two containerized services:

- **Gateway Service (FastAPI)**  
  - Entry point for clients (`/api/v1/data`)  
  - Implements Circuit Breaker, Retry, Rate Limiting  
  - Exposes `/health` and `/metrics`  

- **Flaky Backend Service (FastAPI)**  
  - Endpoint `/flaky-data` randomly returns:  
    - ✅ 200 OK (~60%)  
    - ❌ 503 Service Unavailable (~20%)  
    - ⏱️ Artificial delay (~20%)  

### Diagram
```mermaid
flowchart LR
    C[Client] --> G[API Gateway<br/>(FastAPI)]
    G --> B[Flaky Backend<br/>(FastAPI)]

    G --> CB[Circuit Breaker]
    G --> RT[Retry + Exponential Backoff]
    G --> RL[Rate Limiting]
    G --> OBS[/health + /metrics]
---

## ⚙️ Configuration
All parameters are configurable via environment variables (`.env`):

| Variable | Description | Example |
|----------|-------------|---------|
| `FLAKY_SERVICE_URL` | URL of backend service | `http://flaky_backend:8001/flaky-data` |
| `FAILURE_THRESHOLD` | Failures before circuit opens | `3` |
| `RECOVERY_TIMEOUT_SECONDS` | Timeout before half‑open | `10` |
| `TEST_REQUESTS_ALLOWED_HALF_OPEN` | Requests allowed in half‑open | `1` |
| `MAX_RETRIES` | Max retry attempts | `3` |
| `INITIAL_BACKOFF_SECONDS` | Initial backoff | `0.5` |
| `BACKOFF_MULTIPLIER` | Backoff multiplier | `2.0` |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `True` |
| `RATE_LIMIT_REQUESTS_PER_WINDOW` | Requests per window | `5` |
| `RATE_LIMIT_WINDOW_SECONDS` | Window size (seconds) | `60` |

👉 See `.env.example` for default values.
---

## 🔧 Setup & Run

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/my-api-gateway.git
cd my-api-gateway

### ✅ 2. Build and Start Services 
```bash 
docker-compose up --build -d

### ✅ 3. Check Running Containers
```bash
docker-compose ps
### ✅ 4. Verify Health Endpoints
Run these commands in your terminal (VS Code / Git Bash / PowerShell):

```bash
curl http://localhost:8000/health
curl http://localhost:8001/flaky-data

### ✅ 5. Call the main API endpoint (Gateway)
```bash
curl -i http://localhost:8000/api/v1/data

### ✅ 6. View Metrics
**Raw metrics:**
```bash
curl -s http://localhost:8000/metrics
**Pretty-print metrics (if jq is not installed):**
```bash
curl -s http://localhost:8000/metrics | python -m json.tool
**Save metrics to file:**
```bash
curl -s http://localhost:8000/metrics > metrics.json  

### ✅ 7. Run Tests
**Run unit tests:**
```bash
docker-compose exec gateway pytest tests/unit -v
**Run integration tests:**
```bash
docker-compose exec gateway pytest tests/integration -v
**Run all tests:**
```bash
docker-compose exec gateway pytest tests -v

### ✅ 8. Run Automated Verification Script (Recommended)
```bash
./verify.sh

### ✅ 9. Stop Services
```bash
docker-compose down

---

## 🌐 API Endpoints

### ✅ Gateway Service
- `GET /api/v1/data`  
  → Proxies requests to the flaky backend with resilience patterns (circuit breaker, retry, rate limiting).  
- `GET /health`  
  → Returns **200 OK** if the gateway is healthy.  
- `GET /metrics`  
  → Provides resilience metrics (**circuit breaker state, retries, rate limit stats**).  

### ✅ Flaky Backend Service
- `GET /flaky-data`  
  → Randomly returns:
    - ✅ `200 OK` (~60%)  
    - ❌ `503 Service Unavailable` (~20%)  
    - ⏱️ Artificial delay (~20%)  

---

## 📊 Metrics Example

Snapshot saved in `metrics.json` after running `verify.sh`:

```json
{
  "circuit_breaker_state": "OPEN",
  "total_retries": 6,
  "rate_limit_allowed": 5,
  "rate_limit_blocked": 10
}

---

## ⚡ Circuit Breaker States

The gateway implements a **Circuit Breaker** to protect the flaky backend.  
It transitions through **three states**:

| State       | Description                                                                 | Transition Trigger                                      |
|-------------|-----------------------------------------------------------------------------|---------------------------------------------------------|
| **CLOSED**  | Normal operation. Requests flow to the backend. Failures are counted.       | Backend failures reach threshold → move to **OPEN**     |
| **OPEN**    | Gateway immediately rejects calls to backend (returns **503**). Prevents overload. | Timeout expires → move to **HALF-OPEN**                 |
| **HALF-OPEN** | Gateway allows a limited number of test requests to check backend recovery. | If test succeeds → move to **CLOSED**; if test fails → back to **OPEN** |

---

## 📂 Project Structure

my-api-gateway/
├── gateway_service/
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── flaky_service/
│   ├── src/
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── verify.sh
├── metrics.json
└── README.md

---

## 📜 License

This project is released under the **MIT License**.  
You are free to use, modify, and distribute this software with proper attribution.
