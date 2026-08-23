"""Simulates a routing decision for an incoming packet/request."""

from intelligence.strategy import get_strategy
from memory.db import log_event

ROUTE_BY_MODE = {
    "conservative": "safe-path",
    "aggressive": "fast-path",
    "cautious": "standard-path",
    "balanced": "standard-path",
}


def send_packet(data: dict) -> dict:
    """Decide how a packet should be routed under the current strategy.

    This doesn't move real network traffic — it's the decision layer
    of the simulation: given the engine's current strategy/mode, it
    picks a route class and logs the decision, so the router is
    genuinely driven by the rest of the system rather than acting in
    isolation.
    """
    strategy = get_strategy()
    mode = strategy["mode"]
    route = ROUTE_BY_MODE.get(mode, "standard-path")

    decision = {
        "received": data,
        "route": route,
        "strategy": strategy["strategy"],
        "mode": mode,
    }
    log_event("packet_routed", f"route={route} mode={mode}")
    return decision
