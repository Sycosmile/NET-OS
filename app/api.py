from fastapi import APIRouter

from intelligence.health import system_health
from intelligence.strategy import get_strategy
from intelligence.predictor import predict_load
from intelligence.behavior import analyze_behavior
from core.engine import run_engine
from router.client import send_packet
from memory.db import fetch_recent_metrics, fetch_recent_events

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return system_health()


@router.get("/strategy")
def strategy():
    return get_strategy()


@router.get("/predict")
def predict():
    return predict_load()


@router.get("/behavior")
def behavior():
    return analyze_behavior()


@router.get("/engine")
def engine():
    """Trigger one engine tick on demand and return the full result."""
    return run_engine()


@router.get("/history")
def history(limit: int = 20):
    return {
        "metrics": fetch_recent_metrics(limit=limit),
        "events": fetch_recent_events(limit=limit),
    }


@router.post("/route")
def route(data: dict):
    """Simulate routing a packet under the current strategy."""
    return send_packet(data)
