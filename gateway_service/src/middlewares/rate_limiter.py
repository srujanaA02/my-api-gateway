import time
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.clients = {}

    def check(self, client_id):
        now = time.time()
        window_start = now - self.window
        self.clients.setdefault(client_id, [])
        self.clients[client_id] = [
            t for t in self.clients[client_id] if t > window_start
        ]
        if len(self.clients[client_id]) >= self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        self.clients[client_id].append(now)
