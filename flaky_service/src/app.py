import random
import time
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/flaky-data")
def flaky_data():
    roll = random.randint(1, 10)  # random number 1–10

    if roll <= 6:  # ~60% chance success
        return {"message": "Data retrieved successfully"}
    elif roll <= 8:  # ~20% chance failure
        raise HTTPException(status_code=503, detail="Forced failure")
    else:  # ~20% chance delay
        time.sleep(1)  # simulate delay
        return {"message": "Delayed success"}
