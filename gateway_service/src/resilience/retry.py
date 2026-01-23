import time

retry_stats = {"total_retries": 0}

async def retry(operation, max_retries=3, backoff=0.5, multiplier=2.0):
    delay = backoff
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            retry_stats["total_retries"] += 1
            await async_sleep(delay)
            delay *= multiplier

async def async_sleep(seconds):
    import asyncio
    await asyncio.sleep(seconds)