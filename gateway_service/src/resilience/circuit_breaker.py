import time
from enum import Enum

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout, test_requests):
        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.test_requests = test_requests
        self.half_open_attempts = 0

    def can_request(self):
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = State.HALF_OPEN
                self.half_open_attempts = 0
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        self.state = State.CLOSED

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = State.OPEN
            self.last_failure_time = time.time()
