import time

def retry(operation, max_retries, backoff, multiplier):
    delay = backoff
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= multiplier
