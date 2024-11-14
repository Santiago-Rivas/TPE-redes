from fastapi import FastAPI
import time
import random

app = FastAPI()


@app.get("/")
async def delayed_response():
    # Randomly choose between 1, 5 and 10 seconds for response delay
    delay = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    time.sleep(delay)
    return {"message": f"Response delayed by {delay} seconds"}
