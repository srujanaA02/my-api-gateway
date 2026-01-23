import time

rate_limiter_stats = {"allowed": 0, "blocked": 0}

class RateLimiter:
    def __init__(self, limit=5, window_seconds=60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = {}

    def allow_request(self, client_id):
        now = time.time()
        window_start = now - self.window_seconds
        self.requests.setdefault(client_id, [])
        self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]

        if len(self.requests[client_id]) < self.limit:
            self.requests[client_id].append(now)
            rate_limiter_stats["allowed"] += 1
            return True
        else:
            rate_limiter_stats["blocked"] += 1
            return False

rate_limiter = RateLimiter()