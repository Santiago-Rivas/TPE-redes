from fastapi import FastAPI
import time
import random

app = FastAPI()

@app.get("/")
async def delayed_response():
    # Randomly choose between 1, 5 and 10 seconds for response delay
    delay = random.choice([1, 5, 10])
    time.sleep(delay)
    return {"message": f"Response delayed by {delay} seconds"}
