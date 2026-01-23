import pytest
from resilience.retry import retry, retry_stats

@pytest.mark.asyncio
async def test_retry_success():
    calls = {"count": 0}

    async def flaky_op():
        calls["count"] += 1
        if calls["count"] < 2:
            raise Exception("Transient error")
        return "success"

    result = await retry(flaky_op, max_retries=3, backoff=0.1, multiplier=2)
    assert result == "success"
    assert retry_stats["total_retries"] >= 1