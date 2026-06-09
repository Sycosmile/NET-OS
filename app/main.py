from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Net-OS")

app.include_router(router)

@app.get("/")
def root():
    return {"status": "Net-OS running"}
