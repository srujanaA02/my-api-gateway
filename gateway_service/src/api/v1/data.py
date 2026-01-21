import requests
from fastapi import APIRouter, Request, HTTPException
from config import *
from resilience.circuit_breaker import CircuitBreaker
from resilience.retry import retry
from middlewares.rate_limiter import RateLimiter

router = APIRouter()

cb = CircuitBreaker(
    FAILURE_THRESHOLD,
    RECOVERY_TIMEOUT,
    TEST_REQUESTS_ALLOWED
)

rate_limiter = RateLimiter(
    RATE_LIMIT,
    RATE_WINDOW
)

@router.get("/data")
def get_data(request: Request):
    client_ip = request.client.host
    rate_limiter.check(client_ip)

    if not cb.can_request():
        raise HTTPException(
            status_code=503,
            detail="Circuit breaker open"
        )

    def call_backend():
        r = requests.get(FLAKY_URL, timeout=2)

        if r.status_code >= 500:
            raise HTTPException(
                status_code=503,
                detail="Backend service unavailable"
            )

        return r.json()

    try:
        result = retry(
            call_backend,
            MAX_RETRIES,
            INITIAL_BACKOFF,
            BACKOFF_MULTIPLIER
        )
        cb.record_success()
        return result

    except HTTPException:
        cb.record_failure()
        raise HTTPException(
            status_code=503,
            detail="Backend failure"
        )
