from fastapi import APIRouter
from intelligence.health import system_health
from intelligence.strategy import get_strategy

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return system_health()

@router.get("/strategy")
def strategy():
    return get_strategy()
