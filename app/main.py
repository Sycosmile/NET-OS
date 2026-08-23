from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import router
from memory.db import init_db
from workers.daemon import start_daemon, stop_daemon


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: prepare storage and kick off the background engine loop
    init_db()
    start_daemon(interval=5.0)
    yield
    # Shutdown: signal the background loop to stop
    stop_daemon()


app = FastAPI(title="Net-OS", lifespan=lifespan)

app.include_router(router)
app.mount("/dashboard", StaticFiles(directory="dashboard", html=True))


@app.get("/")
def root():
    return {"status": "Net-OS running"}
