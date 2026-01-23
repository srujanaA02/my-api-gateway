import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10, test_requests_allowed=1):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.test_requests_allowed = test_requests_allowed
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = None
        self.test_requests = 0

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
        self.test_requests = 0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def check_state(self):
        if self.state == "OPEN" and self.last_failure_time:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "HALF-OPEN"
                self.test_requests = 0

    def allow_request(self):
        self.check_state()
        if self.state == "OPEN":
            return False
        elif self.state == "HALF-OPEN":
            if self.test_requests < self.test_requests_allowed:
                self.test_requests += 1
                return True
            else:
                return False
        return True

# Export global instance
circuit_breaker = CircuitBreaker()