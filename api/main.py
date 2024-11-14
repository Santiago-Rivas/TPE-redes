from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import redis
from contextlib import contextmanager

# Initialize FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Connect to Redis server
r = redis.Redis(host='redis', port=6379, db=0)

# Create a context manager to handle Redis locks


@app.on_event("startup")
async def startup():
    # Flush all Redis data
    try:
        r.flushall()
        print("Redis cache cleared")
    except Exception as e:
        print(f"Error clearing Redis cache: {e}")


@contextmanager
def redis_lock(lock_name, timeout=10):
    # Try to acquire the lock
    lock = r.lock(lock_name, timeout=timeout)
    acquired = lock.acquire(blocking=False)
    if acquired:
        try:
            yield lock  # Control is passed to the code inside the `with` block
        finally:
            lock.release()  # Ensure the lock is released
    else:
        # If we can't acquire the lock
        raise Exception("Could not acquire lock")


@app.get("/front")
def get_frontend():
    return HTMLResponse(open("static/index.html").read())


@app.get("/")
def read_root():
    try:
        with redis_lock('counter_lock'):
            # Critical section: Only one worker can execute this at a time
            r.incr('counter')  # Atomically increment the counter in Redis
            return {"Hello": "World"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/status")
def status():
    try:
        with redis_lock('counter_lock'):
            r.incr('counter')  # Atomically increment the counter in Redis
            return {"status": "up"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    try:
        with redis_lock('counter_lock'):
            r.incr('counter')  # Atomically increment the counter in Redis
            return {"health": "ok"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/metrics")
def metrics():
    try:
        with redis_lock('counter_lock'):
            r.incr('counter')  # Atomically increment the counter in Redis
            counter = int(r.get('counter') or 0)
            if counter > 5:
                return {"metrics": "no_data"}
            else:
                return {"metrics": "data"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/count")
def count():
    try:
        with redis_lock('counter_lock'):
            counter = int(r.get('counter') or 0)
            return {"count": counter}
    except Exception as e:
        return {"error": str(e)}


@app.get("/reset")
def reset():
    try:
        with redis_lock('counter_lock'):
            r.set('counter', 0)  # Reset the counter in Redis to 0
            return {"count": 0}
    except Exception as e:
        return {"error": str(e)}


@app.get("/write")
def write():
    for i in range(100000):
        r.set(f'key_{i}', f'value_{i}')
    return {"status": "100000 writes completed"}


@app.get("/read")
def read():
    # Retrieve all 1000 keys and their values
    data = {f'key_{i}': r.get(f'key_{i}').decode('utf-8') for i in range(1000)}
    return {"data": data}
