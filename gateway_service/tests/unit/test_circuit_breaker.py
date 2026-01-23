import time
from resilience.circuit_breaker import CircuitBreaker

def test_initial_state_closed():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1, test_requests_allowed=1)
    assert cb.state == "CLOSED"

def test_open_after_failures():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1, test_requests_allowed=1)
    cb.record_failure()
    cb.record_failure()
    assert cb.state == "OPEN"

def test_half_open_after_timeout():
    cb = CircuitBreaker(failure_threshold=1, recovery_timeout=1, test_requests_allowed=1)
    cb.record_failure()
    assert cb.state == "OPEN"
    time.sleep(1.1)
    cb.check_state()
    assert cb.state == "HALF-OPEN"