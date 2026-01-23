from fastapi import FastAPI, Request, HTTPException
import httpx
import os

from resilience.circuit_breaker import circuit_breaker
from resilience.retry import retry, retry_stats
from middlewares.rate_limiter import rate_limiter, rate_limiter_stats

app = FastAPI()

FLAKY_SERVICE_URL = os.getenv("FLAKY_SERVICE_URL", "http://flaky_backend:8001/flaky-data")

@app.get("/api/v1/data")
async def get_data(request: Request):
    client_ip = request.client.host

    # Rate limiting
    if not rate_limiter.allow_request(client_ip):
        raise HTTPException(status_code=429, detail="Too Many Requests")

    # Circuit breaker
    if not circuit_breaker.allow_request():
        raise HTTPException(status_code=503, detail="Service Unavailable (circuit open)")

    async def call_backend():
        async with httpx.AsyncClient() as client:
            resp = await client.get(FLAKY_SERVICE_URL, timeout=5)
            if resp.status_code >= 500:
                raise Exception("Transient backend error")
            return resp.json()

    try:
        result = await retry(call_backend)
        circuit_breaker.record_success()
        return result
    except Exception:
        circuit_breaker.record_failure()
        raise HTTPException(status_code=503, detail="Backend failure")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return {
        "circuit_breaker_state": circuit_breaker.state,
        "total_retries": retry_stats.get("total_retries", 0),
        "rate_limit_allowed": rate_limiter_stats.get("allowed", 0),
        "rate_limit_blocked": rate_limiter_stats.get("blocked", 0)
    }