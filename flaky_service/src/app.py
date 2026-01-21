import random
import time
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/flaky-data")
def flaky():
    choice = random.random()

    # ~60% success
    if choice < 0.6:
        return {
            "status": "success",
            "data": "Hello from flaky service"
        }

    # ~20% transient failure
    elif choice < 0.8:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )

    # ~20% delayed success
    else:
        time.sleep(random.uniform(0.5, 1.0))
        return {
            "status": "delayed success"
        }
