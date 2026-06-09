import time

def tick():
    return {"scheduler": "tick"}

def run_loop():
    while True:
        tick()
        time.sleep(5)
