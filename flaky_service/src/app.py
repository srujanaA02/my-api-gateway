from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/flaky-data")
def flaky_data():
    raise HTTPException(status_code=503, detail="Forced failure")