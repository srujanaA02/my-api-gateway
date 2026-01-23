import pytest
from middlewares.rate_limiter import RateLimiter

def test_rate_limit_blocks_after_threshold():
    rl = RateLimiter(limit=2, window_seconds=60)
    client = "127.0.0.1"
    assert rl.allow_request(client)
    assert rl.allow_request(client)
    assert not rl.allow_request(client)  # third request blocked