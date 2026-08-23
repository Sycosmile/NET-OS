"""Chooses an operating strategy from current health and load trend."""

from intelligence.health import system_health
from intelligence.predictor import predict_load


def get_strategy() -> dict:
    """Pick a routing/operating strategy based on live conditions.

    - critical health -> defensive-throttling (protect the system first)
    - rising load + degraded health -> proactive-scaling
    - otherwise -> adaptive-routing (normal balanced operation)
    """
    health = system_health()
    prediction = predict_load()

    overall = health["overall"]
    trend = prediction["prediction"]

    if overall == "critical":
        strategy = "defensive-throttling"
        mode = "conservative"
    elif overall == "degraded" and trend == "rising":
        strategy = "proactive-scaling"
        mode = "aggressive"
    elif overall == "degraded":
        strategy = "adaptive-routing"
        mode = "cautious"
    else:
        strategy = "adaptive-routing"
        mode = "balanced"

    return {
        "strategy": strategy,
        "mode": mode,
        "based_on": {
            "health": overall,
            "trend": trend,
        },
    }
